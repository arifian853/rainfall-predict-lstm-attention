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
} from "@/components/ui/table"


export const Prediction = () => {
  const [inputData, setInputData] = useState(Array(10).fill({ Tavg: '', RH_avg: '', ss: '', ff_avg: '' }));
  const [predictions, setPredictions] = useState({ lstm: null, lstm_attention: null });
  const [loading, setLoading] = useState(false)
  const [date, setDate] = useState('')


  const handleChange = (index: number, event: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    const updatedInputData = inputData.map((day, i) => (
      i === index ? { ...day, [name]: value } : day
    ));
    setInputData(updatedInputData);
  };

  const handleSubmit = async (event: { preventDefault: () => void }) => {
    setLoading(true);
    event.preventDefault();
    const response = await fetch('https://flask-example.1hrnom1bxkr4.us-south.codeengine.appdomain.cloud/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ input: inputData }),
    });

    const data = await response.json();
    setPredictions({
      lstm: data.predictions_lstm,
      lstm_attention: data.predictions_lstm_attention,
    });
    toast.success('Predicted!');
    setLoading(false);
  };

  return (
    <div className="bg-slate-800 text-white h-auto flex flex-col justify-center items-center">
      <div className="p-5 bg-slate-900 flex justify-center items-center w-full">
        <h1 className="text-xl">Rainfall Prediction</h1>
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
        <p className="m-5">Fill 10 days ago weather data</p>
        {inputData.map((day, index) => (
          <div key={index} className="bg-slate-800 flex flex-row items-center p-3 gap-3 border rounded-md mb-5 shadow-lg">
            <h3 className="w-16 text-sm">Day {index + 1}</h3>
            <div className="flex flex-col gap-2">
              <div className="w-56 flex flex-col gap-2">
                <span className="text-sm">Average Temperature (°C)</span>
                <Input
                  type="number"
                  name="Tavg"
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

          <Button className='hover:border w-[100px]' type="submit">Predict</Button>
        </div>
        <Toaster />
      </form>
      <p className="m-5">Prediction result :</p>
      {
        loading ?
          (
            <> <p>Predicting...</p> <span className="loader"> </span> </>
          ) : (
            <div className="border p-3 mb-5 rounded-md">
              <p>Date : {date}</p>
              <Table className="w-[530px]">
                <TableHeader>

                  <TableRow>
                    <TableHead className="w-1/2 text-green-500">Algorithm</TableHead>
                    <TableHead className="w-1/2 text-green-500">Predicted Rainfall (rr)</TableHead>
                  </TableRow>

                </TableHeader>

                <TableBody>

                  <TableRow>
                    <TableCell className="font-medium">Regular LSTM</TableCell>
                    <TableCell><span className="text-green-500 underline">{predictions.lstm}</span> mm</TableCell>
                  </TableRow>

                  <TableRow>
                    <TableCell className="font-medium">LSTM With Attention</TableCell>
                    <TableCell> <span className="text-green-500 underline">{predictions.lstm_attention}</span> mm</TableCell>
                  </TableRow>

                </TableBody>

              </Table>
            </div>
          )
      }
      <Link to='/'>
        <Button className='hover:border w-[100px]'> Home </Button>
      </Link>
      <br /><br />
    </div>
  );
};
