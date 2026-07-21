import api from "./api";

export const getMetrics = async () => {
    const response = await api.get("/metrics");
    return response.data;
};