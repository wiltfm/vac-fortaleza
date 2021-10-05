import React, { useEffect, useState } from 'react';
import { Grid } from 'antd';
import Marquee from './Marquee';

import { getLastSpreadsheetsProcessed } from '../services/Api';

const { useBreakpoint } = Grid;

export default function SheetsMarquee() {
    const [lastSheets, setLastSheets] = useState([]);

    useEffect(() => {
        const asyncGetProcessedSpreadsheets = async () => {
            try {
                const response = await getLastSpreadsheetsProcessed();
                const data = await response.json();
                setLastSheets(data.results);
            } catch (error) {
                console.error(error);
            }
        }

        asyncGetProcessedSpreadsheets();
    }, [])

    const screens = useBreakpoint();
    const md = !!screens.md;

    if (!lastSheets.length) return null;

    const Message = () => <span>
        Últimas listas processadas:{" "}
        {lastSheets.map(sheet => sheet.name).join(', ')}
    </span>;

    return (
        <div>
            {md ? (
                <Message />
            ) : (
                <Marquee>
                    <Message />
                </Marquee>
            )}
        </div>
    )
}
