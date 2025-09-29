import { Routes } from '@angular/router';
import { MainPage } from './components/main-page/main-page';
import { DetailsPage } from './components/details-page/details-page';

export const routes: Routes = [
  {
    path: '',
    component: MainPage,
  },
  {
    path: 'details/:id',
    component: DetailsPage,
  },
];
