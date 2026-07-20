from supabase_client import supabase


def get_all_kpis():

    response = (
        supabase
        .table("metrics")
        .select("*")
        .execute()
    )

    return response.data


def get_kpi_by_metric_id(metric_id):

    response = (
        supabase
        .table("metrics")
        .select("*")
        .eq("metric_id", metric_id)
        .execute()
    )

    return response.data


def get_kpi_by_name(metric_name):

    response = (
        supabase
        .table("metrics")
        .select("*")
        .eq("metric_name", metric_name)
        .execute()
    )

    return response.data


def get_kpis_by_sheet(sheet_name):

    response = (
        supabase
        .table("metrics")
        .select("*")
        .eq("sheet_name", sheet_name)
        .execute()
    )

    return response.data


def get_kpis_by_abbreviation(abbreviation):

    response = (
        supabase
        .table("metrics")
        .select("*")
        .eq("abbreviation", abbreviation)
        .execute()
    )

    return response.data


def get_latest_kpis(limit=20):

    response = (
        supabase
        .table("metrics")
        .select("*")
        .order("id", desc=True)
        .limit(limit)
        .execute()
    )

    return response.data


if __name__ == "__main__":

    print("\n----- ALL KPI COUNT -----")
    all_kpis = get_all_kpis()
    print(len(all_kpis))

    print("\n----- METRIC ID 1 -----")
    print(get_kpi_by_metric_id(1))

    print("\n----- NII -----")
    print(get_kpis_by_abbreviation("nii"))

    print("\n----- REVENUE -----")
    print(get_kpi_by_name("revenue"))

    print("\n----- LATEST 5 -----")
    print(get_latest_kpis(5))