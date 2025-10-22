import { Routes } from '@angular/router';
import { LoginComponent } from './views/auth/login/login.component';
import { RegisterUserComponent } from './views/auth/register-user/register-user.component';
import { LayoutComponent } from './components/layout/layout.component';
import { HomeComponent } from './views/home/home.component';
import { ViewAllUsersComponent } from './views/user/view-all-users/view-all-users.component';
import { ViewUserByIdComponent } from './views/user/view-user-by-id/view-user-by-id.component';

export const routes: Routes = [
    {
        path: '',
        redirectTo: 'login',
        pathMatch: 'full'
    },
    { path: 'login', component: LoginComponent },
    { path: 'register', component: RegisterUserComponent },
    {
        path: '', component: LayoutComponent, children: [
            { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
            { path: 'home', component: HomeComponent },
            { path: 'clients', component: ViewAllUsersComponent },
            { path: 'user/:userId', component: ViewUserByIdComponent },
        ]
    }
];
