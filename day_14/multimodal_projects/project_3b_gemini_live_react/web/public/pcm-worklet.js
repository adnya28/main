// Runs on the browser's AUDIO thread, not the UI thread - so a busy page never
// stutters the microphone. It does one job: collect the tiny 128-sample blocks
// the browser hands it into ~100ms parcels and post them to the page.
const CHUNK = 1600; // 100ms at 16kHz

class PCMCollector extends AudioWorkletProcessor {
  constructor() {
    super();
    this.buffer = new Float32Array(CHUNK);
    this.filled = 0;
  }

  process(inputs) {
    const channel = inputs[0]?.[0];
    if (!channel) return true;
    for (let i = 0; i < channel.length; i++) {
      this.buffer[this.filled++] = channel[i];
      if (this.filled === CHUNK) {
        this.port.postMessage(this.buffer.slice(0));
        this.filled = 0;
      }
    }
    return true; // never stop
  }
}

registerProcessor("pcm-collector", PCMCollector);
