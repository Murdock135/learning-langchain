
def save_graph(save_path, graph_obj):
    with open(save_path, "wb") as f:
        f.write(graph_obj.get_graph().draw_mermaid_png())
