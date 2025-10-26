import { Routes } from '@angular/router';
import { LoginComponent } from './views/auth/login/login.component';
import { RegisterUserComponent } from './views/auth/register-user/register-user.component';
import { LayoutComponent } from './components/layout/layout.component';
import { HomeComponent } from './views/home/home.component';
import { ViewAllUsersComponent } from './views/user/view-all-users/view-all-users.component';
import { ViewUserByIdComponent } from './views/user/view-user-by-id/view-user-by-id.component';
import { AdminDashboardComponent } from './views/dashboard/admin-dashboard/admin-dashboard.component';
import { ClientDashboardComponent } from './views/dashboard/client-dashboard/client-dashboard.component';
import { UserVerificationApplicationComponent } from './views/user/user-verification-application/user-verification-application.component';
import { UserAccountManagerComponent } from './views/user/user-account-manager/user-account-manager.component';
import { ViewAllNotificationsComponent } from './views/notification/view-all-notifications/view-all-notifications.component';
import { CameraComponent } from './views/camera/camera.component';

export const routes: Routes = [
    {
        path: '',
        redirectTo: 'login',
        pathMatch: 'full'
    },
    { path: 'login', component: LoginComponent },
    { path: 'register', component: RegisterUserComponent },
    { path: 'camera', component: CameraComponent },
    {
        path: '', component: LayoutComponent, children: [
            { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
            { path: 'home', component: HomeComponent },
            { path: 'admin-dashboard', component: AdminDashboardComponent },
            { path: 'client-dashboard', component: ClientDashboardComponent },
            { path: 'clients', component: ViewAllUsersComponent },
            { path: 'user/:userId', component: ViewUserByIdComponent },
            { path: 'verify-account', component: UserVerificationApplicationComponent },
            { path: 'account', component: UserAccountManagerComponent },
            { path: 'notifications', component: ViewAllNotificationsComponent },
        ]
    }
];
