from workspace_conf import workspaces,rooms,get_group_name

class WorkspaceState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WorkspaceState, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.wsp = {
            'current': workspaces[0][0],  # Espace de travail par défaut
        }

    def update(self, new_state):
        self.wsp.update(new_state)
        for w, _ in workspaces:
            self.wsp[w] = {
                'active_group': get_group_name(w, rooms[0]) # first room is active by default
            }

    def get(self):
        return self.wsp

    def set_current(self, workspace):
        self.wsp['current'] = workspace

    def get_current(self):
        return self.wsp['current']

    def set_active_group(self, workspace, group):
        if workspace not in self.wsp:
            self.wsp[workspace] = {}
        self.wsp[workspace]['active_group'] = group

    def get_active_group(self, workspace):
        return self.wsp.get(workspace, {}).get('active_group')

# Créer une instance globale
workspace_state = WorkspaceState()