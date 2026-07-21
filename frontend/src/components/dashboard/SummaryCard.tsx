type Props = {

    title: string;

    value: string | number;

};

export default function SummaryCard({

    title,

    value,

}: Props) {

    return (

        <div className="bg-white rounded-xl shadow p-5">

            <div className="text-sm text-gray-500">

                {title}

            </div>

            <div className="text-3xl font-bold mt-2">

                {value}

            </div>

        </div>

    );

}   