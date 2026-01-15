from langgraph.graph import StateGraph, END
from app.state import TravelState
from app.agents.receptionist import receptionist_agent
from app.agents.flight_agent import flight_agent
from app.agents.hotel_agent import hotel_agent
from app.agents.itinerary_agent import itinerary_agent

def build_graph():
    graph = StateGraph(TravelState)

    graph.add_node("receptionist", receptionist_agent)
    graph.add_node("flight", flight_agent)
    graph.add_node("hotel", hotel_agent)
    graph.add_node("itinerary", itinerary_agent)

    graph.set_entry_point("receptionist")

    graph.add_edge("receptionist", "flight")
    graph.add_edge("flight", "hotel")
    graph.add_edge("hotel", "itinerary")
    graph.add_edge("itinerary", END)

    return graph.compile()
