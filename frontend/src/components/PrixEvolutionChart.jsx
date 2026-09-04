import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

function PrixEvolutionChart({ data }) {
  const groupesParDate = {};

  for (const item of data) {
    const date = item.date_releve;

    if (!groupesParDate[date]) {
      groupesParDate[date] = [];
    }

    groupesParDate[date].push(Number(item.prix_moyen));
  }

  const chartData = Object.entries(groupesParDate)
    .map(([date, prix]) => {
      const moyenne =
        prix.reduce(
          (total, valeur) => total + valeur,
          0,
        ) / prix.length;

      return {
        date: new Date(date).toLocaleDateString("fr-FR"),
        prix: moyenne,
      };
    })
    .sort(
      (a, b) =>
        new Date(a.date.split("/").reverse().join("-")) -
        new Date(b.date.split("/").reverse().join("-")),
    );

  if (chartData.length === 0) {
    return (
      <div className="rounded-xl bg-gray-50 p-6 text-center text-gray-500">
        Aucune donnée disponible pour afficher l'évolution
        des prix.
      </div>
    );
  }

  return (
    <div className="w-full">
      <div className="h-72 w-full sm:h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={chartData}
            margin={{
              top: 10,
              right: 20,
              left: 0,
              bottom: 10,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />

            <XAxis
              dataKey="date"
              tick={{ fontSize: 12 }}
            />

            <YAxis
              tick={{ fontSize: 12 }}
              tickFormatter={(value) =>
                `${value} FCFA`
              }
            />

            <Tooltip
              formatter={(value) => [
                `${Number(value).toLocaleString(
                  "fr-FR",
                  {
                    maximumFractionDigits: 0,
                  },
                )} FCFA`,
                "Prix moyen",
              ]}
              labelFormatter={(label) =>
                `Date : ${label}`
              }
              contentStyle={{
                borderRadius: "8px",
                border: "1px solid #e5e7eb",
              }}
            />

            <Line
              type="monotone"
              dataKey="prix"
              stroke="#15803d"
              strokeWidth={3}
              dot={{ r: 5 }}
              activeDot={{ r: 7 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <p className="mt-3 text-center text-xs text-gray-500">
        Évolution du prix moyen selon les relevés OMA.
      </p>
    </div>
  );
}

export default PrixEvolutionChart;