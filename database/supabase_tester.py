from database.SupabaseManager import SupabaseManager

def test_supabase():
    supabase_manager = SupabaseManager()
    supabase_manager.add_playlist("1234567890", "Test Subject", "Test Source")
    print(supabase_manager.get_playlist("1234567890"))
    supabase_manager.add_video("1234567890", "Test Video", "Test Description", "2021-01-01", "10:25", "1234567890")
    print(supabase_manager.get_video("1234567890"))

if __name__ == "__main__":
    test_supabase()