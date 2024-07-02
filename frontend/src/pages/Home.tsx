import { Button } from '@/components/ui/button';
import { Link } from 'react-router-dom';
import { FaCloudRain } from "react-icons/fa";

export const Home = () => {
    return (
        <div className='h-screen flex flex-col justify-center items-center bg-slate-800 gap-5 text-white'>
            <h1 className='text-3xl'>Rainfall Prediction with LSTM + Attention Mechanism</h1>
            <p className='text-sm'>By <a className='underline' href="https://github.com/arifian853" target='blank'>Arifian Saputra</a> (2001020029)</p>
            <Link to='/predict'>
                <Button className='hover:border flex flex-row items-center justify-center gap-2'>
                    Predict Now <FaCloudRain />
                </Button>
            </Link>
        </div>
    )
}
