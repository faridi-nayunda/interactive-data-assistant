import React from "react";
import { Bar, Line, Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

export default function DashboardChart({ chart }) {
  if (!chart) return null;

  /* =========================
     KPI CARD
  ========================== */
  if (chart.type === "kpi") {
    return (
      <div className="p-6 bg-linear-to-br from-blue-50 to-indigo-50 rounded-xl text-center border border-blue-100">
        <h2 className="text-sm font-medium text-gray-600 uppercase tracking-wide">
          {chart.label}
        </h2>
        <p className="text-3xl font-bold text-gray-900 mt-2">
          {Number(chart.value).toLocaleString()}
        </p>
      </div>
    );
  }

  /* =========================
     SIMPLE BAR / LINE
  ========================== */
  if (chart.type === "bar" || chart.type === "line") {
    const data = {
      labels: chart.x,
      datasets: [
        {
          label: chart.y_label || "Value",
          data: chart.y,
          backgroundColor: "rgba(59, 130, 246, 0.4)",
          borderColor: "rgb(59, 130, 246)",
          borderWidth: 2,
          fill: chart.type === "line",
          tension: 0.3,
        },
      ],
    };

    return (
      <div className="h-72">
        {chart.type === "bar" ? (
          <Bar data={data} />
        ) : (
          <Line data={data} />
        )}
      </div>
    );
  }

  /* =========================
     PIE CHART
  ========================== */
  if (chart.type === "pie") {
    const data = {
      labels: chart.labels,
      datasets: [
        {
          data: chart.values,
          backgroundColor: [
            "#3b82f6",
            "#6366f1",
            "#8b5cf6",
            "#06b6d4",
            "#10b981",
            "#f59e0b",
          ],
        },
      ],
    };

    return (
      <div className="h-72">
        <Pie data={data} />
      </div>
    );
  }

  /* =========================
     STACKED BAR
  ========================== */
  if (chart.type === "stacked_bar") {
    const data = {
      labels: chart.categories,
      datasets: chart.series.map((serie, index) => ({
        label: serie.name,
        data: serie.data,
        backgroundColor: [
          "#3b82f6",
          "#6366f1",
          "#8b5cf6",
          "#06b6d4",
          "#10b981",
          "#f59e0b",
        ][index % 6],
      })),
    };

    const options = {
      responsive: true,
      scales: {
        x: { stacked: true },
        y: { stacked: true, beginAtZero: true },
      },
    };

    return (
      <div className="h-72">
        <Bar data={data} options={options} />
      </div>
    );
  }

  /* =========================
     GROUPED BAR
  ========================== */
  if (chart.type === "grouped_bar") {
    const data = {
      labels: chart.categories,
      datasets: chart.series.map((serie, index) => ({
        label: serie.name,
        data: serie.data,
        backgroundColor: [
          "#3b82f6",
          "#6366f1",
          "#8b5cf6",
          "#06b6d4",
          "#10b981",
          "#f59e0b",
        ][index % 6],
      })),
    };

    return (
      <div className="h-72">
        <Bar data={data} />
      </div>
    );
  }

  /* =========================
     TABLE
  ========================== */
  if (chart.type === "table") {
    if (!chart.data.length) return null;

    return (
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              {Object.keys(chart.data[0]).map((key) => (
                <th
                  key={key}
                  className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase"
                >
                  {key}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {chart.data.map((row, i) => (
              <tr key={i} className={i % 2 ? "bg-gray-50" : "bg-white"}>
                {Object.values(row).map((val, j) => (
                  <td key={j} className="px-4 py-2 text-sm text-gray-900">
                    {val}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }

  return (
    <div className="text-center py-12 text-gray-500">
      Unsupported chart type
    </div>
  );
}