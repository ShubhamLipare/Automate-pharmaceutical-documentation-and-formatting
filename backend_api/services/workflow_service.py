from graph.workflow import build_graph

def run_workflow(request):

    app = build_graph()

    state = {
        "session_id": request.session_id,
        "user_query": request.user_query,
        "human_feedback": request.human_feedback
    }

    result = app.invoke(state)

    return result["final_report"]