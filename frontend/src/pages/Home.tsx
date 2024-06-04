import { Button } from '@/components/ui/button';
import { Link } from 'react-router-dom';


export const Home = () => {

    return (

        <div className='h-screen flex flex-col justify-center items-center bg-slate-800 gap-5 text-white'>
            <h1 className='text-4xl'>Rainfall Prediction with LSTM Attention</h1>
            <p className='text-sm'>By <a className='underline' href="https://github.com/arifian853" target='blank'>Arifian Saputra</a> (2001020029)</p>
            <Link to='/predict-lstm'>
                <Button className='hover:border'>
                    Predict Now
                </Button>
            </Link>
        </div>

    )
}
