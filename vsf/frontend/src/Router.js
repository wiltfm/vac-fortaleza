import React from 'react';
import { Switch, Route } from 'react-router-dom';
import SearchView from './pages/Search';
import StatsView from './pages/Stats';
import AboutView from './pages/About';
import NotificationView from './pages/EmailNotification';

const RouterKeys = {
  search: '/',
  notification: '/notificacao',
  stats: '/estatistica',
  about: '/sobre',
};

const Router = () => (
  <Switch>
    <Route path={RouterKeys.notification}>
      <NotificationView />
    </Route>
    <Route path={RouterKeys.stats}>
      <StatsView />
    </Route>
    <Route path={RouterKeys.about}>
      <AboutView />
    </Route>
    <Route path="*">
      <SearchView />
    </Route>
  </Switch>
);

export default Router;
export { RouterKeys };
