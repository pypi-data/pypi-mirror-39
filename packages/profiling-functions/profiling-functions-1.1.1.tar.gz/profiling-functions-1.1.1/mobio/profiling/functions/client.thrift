
service ProfilingService {

    string build_query(1: string merchant_id, 2: string business_case_id, 3: string json_pf),
    string add_user(1: string merchant_id, 2: i32 source, 3: string json_str_data, 4: string business_case_id),
    string add_user_b2b(1: string merchant_id, 2: i32 source, 3: string json_str_data, 4: string business_case_id)
}