# what is the state in langgraph?
# A state is 

from typing import TypedDict, NotRequired
from langgraph.graph import StateGraph, START, END

class LoanState(TypedDict):
    applicant: str
    income: float
    emi: float
    ratio: NotRequired[float]

def compute_ratio(state):
    return {"ratio": round(state["emi"] / state["income"], 2)}
#    return {"ratio:": round(state["emi"] / state["income"], 2)}

b = StateGraph(LoanState)
b.add_node("compute_ratio", compute_ratio)
b.add_edge(START, "compute_ratio")
b.add_edge("compute_ratio", END)
graph = b.compile()

print(graph.invoke({"applicant":"Carly", "income":150000,"emi":45000}))


