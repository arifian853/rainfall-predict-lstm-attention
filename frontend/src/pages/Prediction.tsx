/* eslint-disable @typescript-eslint/no-explicit-any */
import { ChangeEvent, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Link } from "react-router-dom";
import toast, { Toaster } from "react-hot-toast";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { MdOutlineKeyboardBackspace } from "react-icons/md";
import { MdFileUpload } from "react-icons/md";

// Default input data
const defaultInputData = [
  { Tavg: 28.7, RH_avg: 83, ss: 4.1, ff_avg: 1 },
  { Tavg: 29.0, RH_avg: 82, ss: 6.0, ff_avg: 2 },
  { Tavg: 28.3, RH_avg: 88, ss: 8.5, ff_avg: 2 },
  { Tavg: 26.8, RH_avg: 93, ss: 5.0, ff_avg: 2 },
  { Tavg: 28.9, RH_avg: 83, ss: 1.5, ff_avg: 2 },
  { Tavg: 28.3, RH_avg: 85, ss: 2.8, ff_avg: 2 },
  { Tavg: 28.3, RH_avg: 87, ss: 4.1, ff_avg: 3 },
  { Tavg: 26.7, RH_avg: 92, ss: 6.2, ff_avg: 2 },
  { Tavg: 27.2, RH_avg: 94, ss: 0.0, ff_avg: 1 },
  { Tavg: 26.6, RH_avg: 94, ss: 3.0, ff_avg: 1 }
];

export const Prediction = () => {
  const [inputData, setInputData] = useState(defaultInputData);
  const [predictions, setPredictions] = useState<{ lstm: string | null, lstm_attention: string | null }>({ lstm: null, lstm_attention: null });
  const [loading, setLoading] = useState(false);
  const [date, setDate] = useState('');

  // Handle change function
  const handleChange = (index: number, event: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    const updatedInputData = inputData.map((day, i) => (
      i === index ? { ...day, [name]: value } : day
      
    ));
    setInputData(updatedInputData);
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);

    try {
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ input: inputData }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch predictions');
      }

      const data = await response.json();
      setPredictions({
        lstm: data.predictions_lstm,
        lstm_attention: data.predictions_lstm_attention,
      });

      toast.success('Predicted!');
    } catch (error) {
      console.error('Prediction fetch error:', error);
      toast.error('Failed to predict. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Function to classify rainfall
  const classifyRainfall = (rainfall: any) => {
    rainfall = parseFloat(rainfall).toFixed(2);
    
    if (rainfall >= 0.1 && rainfall <= 10.0) {
      return `Hujan Ringan`;
    } else if (rainfall > 10.0 && rainfall <= 50.0) {
      return `Hujan Sedang`;
    } else if (rainfall > 50.0 && rainfall <= 100.0) {
      return `Hujan Lebat`;
    } else if (rainfall > 100.0 && rainfall <= 150.0) {
      return `Hujan Sangat Lebat`;
    } else if (rainfall > 150.0) {
      return `Hujan Ekstrem`;
    } else {
      return `Tidak ada hujan/sangat sedikit hujan`;
    }
  };

  return (
    <div className="bg-slate-800 text-white h-auto flex flex-col justify-center items-center">
      <div className="p-5 bg-slate-900 flex justify-center items-center w-full">
        <h1 className="text-xl">Rainfall (RR) Prediction</h1>
      </div>

      <form onSubmit={handleSubmit} className="flex flex-col items-center justify-center p-5">
        <div className="w-[560px] flex flex-col gap-3">
          <p className="text-sm">Pick a date to predict</p>
          <Input
            type="date"
            name="Tavg"
            placeholder="Input date"
            required
            onChange={(e) => setDate(e.target.value)}
          />
        </div>
        <p className="m-5">Fill 10 days {date !== null && date !== undefined && date !== "" ? "before " + date.toLocaleString() : "ago"} weather data</p>
        {inputData.map((day, index) => (
          <div key={index} className="bg-slate-800 flex flex-row items-center p-3 gap-3 border rounded-md mb-5 shadow-lg">
            <h3 className="w-16 text-sm">Day {index + 1}</h3>
            <div className="flex flex-col gap-2">
              <div className="w-56 flex flex-col gap-2">
                <span className="text-sm">Average Temperature (°C)</span>
                <Input
                  type="number"
                  placeholder="Input value"
                  value={day.Tavg}
                  onChange={(e) => handleChange(index, e)}
                  required
                  className="bg-slate-700"
                />
              </div>
              <div className="w-56 flex flex-col gap-2">
                <span className="text-sm">Average Humidity (%)</span>
                <Input
                  type="number"
                  name="RH_avg"
                  placeholder="Input value"
                  value={day.RH_avg}
                  onChange={(e) => handleChange(index, e)}
                  required
                  className="bg-slate-700"
                />
              </div>
            </div>

            <div className="flex flex-col gap-2">
              <div className="w-56 flex flex-col gap-2">
                <span className="text-sm">Sunshine Duration (hours)</span>
                <Input
                  type="number"
                  name="ss"
                  placeholder="Input value"
                  value={day.ss}
                  onChange={(e) => handleChange(index, e)}
                  required
                  className="bg-slate-700"
                />
              </div>
              <div className="w-56 flex flex-col gap-2">
                <span className="text-sm">Average Wind Speed (m/s)</span>
                <Input
                  type="number"
                  name="ff_avg"
                  placeholder="Input value"
                  value={day.ff_avg}
                  onChange={(e) => handleChange(index, e)}
                  required
                  className="bg-slate-700"
                />
              </div>
            </div>
          </div>
        ))}
        <div className="flex gap-3 mt-5">
          <Button className="hover:border w-[100px] flex flex-row justify-center items-center gap-1" type="submit">Predict <MdFileUpload /> </Button>
        </div>
        <Toaster />
      </form>
      {loading !== false ? (
        <>
          <p>Predicting...</p>
          <br />
          <span className="loader"></span>
          <br />
        </>
      ) : (
        predictions.lstm !== null && predictions.lstm_attention !== null && (
          <div className="border p-3 mb-5 rounded-md">
            <p className="text-center pb-2">Rainfall predicted result for {date}</p>
            <hr />
            <Table className="w-[530px]">
              <TableHeader>
                <TableRow className="hover:bg-slate-800">
                  <TableHead className="w-1/2 text-green-500">Algorithm</TableHead>
                  <TableHead className="w-1/2 text-green-500">Predicted Rainfall (rr)</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                <TableRow className="hover:bg-slate-800">
                  <TableCell className="font-medium">Regular LSTM</TableCell>
                  <TableCell>
                    <span className="text-green-500">
                      {parseFloat(predictions.lstm).toFixed(2)} mm - ({classifyRainfall(predictions.lstm)})
                    </span>
                  </TableCell>
                </TableRow>
                <TableRow className="hover:bg-slate-800">
                  <TableCell className="font-medium">LSTM With Attention</TableCell>
                  <TableCell>
                    <span className="text-green-500">
                      {parseFloat(predictions.lstm_attention).toFixed(2)} mm - ({classifyRainfall(predictions.lstm_attention)})
                    </span>
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </div>
        )
      )}

      <Link to="/">
        <Button className="hover:border w-[100px] flex flex-row justify-center items-center gap-2"><MdOutlineKeyboardBackspace /> Home </Button>
      </Link>
      <br /><br />
    </div>
  );
};
