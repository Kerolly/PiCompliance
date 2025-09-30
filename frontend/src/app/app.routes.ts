import { Routes } from '@angular/router';
import { MainPage } from './components/main-page/main-page';
import { DetailsPage } from './components/details-page/details-page';
import { PcPage } from './components/PC-page/pc-page';
import { PhonePage } from './components/phone-page/phone-page';

export const routes: Routes = [
  {
    path: '',
    component: MainPage,
  },
  {
    path: 'others',
    component: DetailsPage,
  },
  {
    path: 'pc',
    component: PcPage,
  },
  {
    path: 'phone',
    component: PhonePage,
  },
];
