import React, { useState } from "react";

const ReportButton = () => {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchReport = async () => {
    setLoading(true);
    try {
      // Формируем GET-запрос к BFF
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/reports/me?from=2025-12-01&to=2025-12-09`,
        {
          method: "GET",
          credentials: "include", // чтобы HttpOnly cookie с токеном ушёл на сервер
        }
      );

      if (!response.ok) {
        throw new Error("Ошибка при получении отчёта");
      }

      const data = await response.json();
      setReport(data);
    } catch (err) {
      console.error(err);
      alert("Не удалось получить отчёт");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ marginTop: "1rem" }}>
      <button onClick={fetchReport} disabled={loading}>
        {loading ? "Загрузка..." : "Получить отчёт"}
      </button>

      {report && (
        <pre style={{ textAlign: "left", marginTop: "1rem" }}>
          {JSON.stringify(report, null, 2)}
        </pre>
      )}
    </div>
  );
};

export default ReportButton;
