import React, { useState, useEffect } from 'react';
import moment from 'moment';
import { Table } from 'antd';

import { getStats } from '../../services/Api';

const StatsView = (props) => {
  const [stats, setStats] = useState([]);
  const [loading, setLoading] = useState([]);

  useEffect(() => {
    const asyncGetStats = async () => {
      setLoading(true);
      try {
        const response = await getStats();
        const data = await response.json();
        setStats(data);
      } catch (error) {
        console.log(error);
      }
      setLoading(false);
    };

    asyncGetStats();
  }, []);

  const columns = [
    {
      title: 'Nome',
      dataIndex: 'spreadsheet__name',
      sorter: (a, b) => moment(a.spreadsheet__date) - moment(b.spreadsheet__date),
      defaultSortOrder: 'descend',
    },
    {
      title: 'Idade Mínima',
      dataIndex: 'birth_date__max',
      render: (value) =>
        `${moment(value).format('L')} - ${moment().diff(moment(value), 'years')} anos`,
      sorter: (a, b) => moment(a.birth_date__max) - moment(b.birth_date__max),
    },
    {
      title: 'Idade Máxima',
      dataIndex: 'birth_date__min',
      render: (value) =>
        `${moment(value).format('L')} - ${moment().diff(moment(value), 'years')} anos`,
      sorter: (a, b) => moment(a.birth_date__min) - moment(b.birth_date__min),
    },
  ];
  return (
    <>
      <Table
        {...props}
        dataSource={stats.by_age}
        columns={columns}
        loading={loading}
        rowKey="spreadsheet__name"
      />
    </>
  );
};

export default StatsView;
