SESSIONS={}

def create(peer_id):
    SESSIONS[peer_id]={"index":0,"vectors":[],"answers":{},"age":None,"medical":None,"profile":None,"results":None,"ai_history":[]}
    return SESSIONS[peer_id]

def get(peer_id): return SESSIONS.get(peer_id)
def reset(peer_id): SESSIONS.pop(peer_id,None)
