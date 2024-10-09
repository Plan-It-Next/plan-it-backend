class Database:
    def __init__(self):

        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY2')

        self.supabase_client = create_client(supabase_url, supabase_key)

    def get_conn(self):
        return self.supabase_client