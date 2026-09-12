/**
 * live.ts — all the audio plumbing, kept away from the React components.
 *
 * Two AudioContexts, because Gemini Live fixes the two rates and they differ:
 *   in  — 16 000 Hz from the microphone, sent as raw PCM16 over the websocket
 *   out — 24 000 Hz from the model, queued so the pieces play back seamlessly
 *
 * The important detail is `echoCancellation`. Without it the microphone hears
 * the assistant's own voice and it interrupts itself forever. With it, you can
 * talk over the assistant and it stops — which is what makes this feel like a
 * phone call rather than a walkie-talkie.
 */

const MIC_RATE = 16000;
const SPEAKER_RATE = 24000;

export type Line = { role: "you" | "bank"; text: string };

export type Handlers = {
  onLine: (line: Line) => void;
  onTurnComplete: () => void;
  onLevel: (rms: number) => void;
  onState: (state: CallState, detail?: string) => void;
};

export type CallState = "idle" | "connecting" | "listening" | "speaking" | "ended";

export class Call {
  private socket?: WebSocket;
  private micCtx?: AudioContext;
  private outCtx?: AudioContext;
  private stream?: MediaStream;
  private queued: AudioBufferSourceNode[] = [];
  private playHead = 0;
  private speaking = false;

  constructor(private on: Handlers) {}

  async start() {
    this.on.onState("connecting");

    // 1. the websocket to server.py, which is holding the Gemini session open
    const url = `${location.protocol === "https:" ? "wss" : "ws"}://${location.host}/ws`;
    const socket = new WebSocket(url);
    socket.binaryType = "arraybuffer";
    this.socket = socket;

    socket.onmessage = (event) => {
      if (event.data instanceof ArrayBuffer) return this.play(new Int16Array(event.data));
      const message = JSON.parse(event.data);
      if (message.role) return this.on.onLine(message as Line);
      if (message.event === "interrupted") return this.stopSpeaking(); // you cut it off
      if (message.event === "turn_complete") {
        this.speaking = false;
        this.on.onState("listening");
        return this.on.onTurnComplete();
      }
    };
    socket.onerror = () => this.on.onState("ended", "the connection failed — is server.py running?");
    socket.onclose = () => this.on.onState("ended");
    await new Promise<void>((ok, fail) => {
      socket.onopen = () => ok();
      setTimeout(() => fail(new Error("server.py did not answer")), 8000);
    });

    // 2. the speaker side — one context, kept at the model's own rate
    this.outCtx = new AudioContext({ sampleRate: SPEAKER_RATE });
    await this.outCtx.resume();

    // 3. the microphone side. Every flag here is doing real work on a live call.
    this.stream = await navigator.mediaDevices.getUserMedia({
      audio: { channelCount: 1, echoCancellation: true, noiseSuppression: true, autoGainControl: true },
    });
    this.micCtx = new AudioContext({ sampleRate: MIC_RATE });
    await this.micCtx.audioWorklet.addModule("/pcm-worklet.js");
    const source = this.micCtx.createMediaStreamSource(this.stream);
    const collector = new AudioWorkletNode(this.micCtx, "pcm-collector");

    collector.port.onmessage = ({ data }: MessageEvent<Float32Array>) => {
      let sum = 0;
      const pcm = new Int16Array(data.length);
      for (let i = 0; i < data.length; i++) {
        const sample = Math.max(-1, Math.min(1, data[i]));
        pcm[i] = sample * 0x7fff; // browsers speak float −1..1; Gemini wants 16-bit ints
        sum += sample * sample;
      }
      this.on.onLevel(Math.sqrt(sum / data.length));
      if (socket.readyState === WebSocket.OPEN) socket.send(pcm.buffer);
    };

    // a worklet only runs while it is part of the graph, so park it on a silent gain node
    const silent = this.micCtx.createGain();
    silent.gain.value = 0;
    source.connect(collector).connect(silent).connect(this.micCtx.destination);

    this.on.onState("listening");
  }

  /** Queue one piece of the reply so it butts up against the piece before it. */
  private play(pcm: Int16Array) {
    const ctx = this.outCtx;
    if (!ctx) return;
    const buffer = ctx.createBuffer(1, pcm.length, SPEAKER_RATE);
    const channel = buffer.getChannelData(0);
    for (let i = 0; i < pcm.length; i++) channel[i] = pcm[i] / 0x8000;

    const node = ctx.createBufferSource();
    node.buffer = buffer;
    node.connect(ctx.destination);
    this.playHead = Math.max(this.playHead, ctx.currentTime + 0.06); // a little slack, so it never gaps
    node.start(this.playHead);
    this.playHead += buffer.duration;
    this.queued.push(node);
    node.onended = () => (this.queued = this.queued.filter((q) => q !== node));

    if (!this.speaking) {
      this.speaking = true;
      this.on.onState("speaking");
    }
  }

  /** Barge-in: drop everything not yet spoken, immediately. */
  private stopSpeaking() {
    this.queued.forEach((node) => {
      try {
        node.stop();
      } catch {
        /* already finished */
      }
    });
    this.queued = [];
    this.playHead = 0;
    this.speaking = false;
    this.on.onState("listening");
  }

  hangUp() {
    this.stopSpeaking();
    this.stream?.getTracks().forEach((track) => track.stop());
    this.micCtx?.close();
    this.outCtx?.close();
    this.socket?.close();
    this.on.onState("idle");
  }
}
