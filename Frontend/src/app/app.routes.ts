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
import { EditUserComponent } from './views/user/edit-user/edit-user.component';
import { ViewAllClaimsComponent } from './views/claim/view-all-claims/view-all-claims.component';
import { ViewClaimsByUserIdComponent } from './views/claim/view-claims-by-user-id/view-claims-by-user-id.component';
import { ViewClaimByIdComponent } from './views/claim/view-claim-by-id/view-claim-by-id.component';
import { ViewAllTemporaryLossApplicationsComponent } from './views/temporary-loss-of-income-protection/view-all-temporary-loss-applications/view-all-temporary-loss-applications.component';
import { ViewTemporaryLossApplicationByIdComponent } from './views/temporary-loss-of-income-protection/view-temporary-loss-application-by-id/view-temporary-loss-application-by-id.component';
import { ExtractTemporaryLossApplicationComponent } from './views/temporary-loss-of-income-protection/extract-temporary-loss-application/extract-temporary-loss-application.component';
import { CameraUserIdComponent } from './views/user/camera-user-id/camera-user-id.component';
import { FreeTextTestComponent } from './views/free-text-test/free-text-test.component';

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
            { path: 'admin-dashboard', component: AdminDashboardComponent },
            { path: 'client-dashboard', component: ClientDashboardComponent },
            { path: 'clients', component: ViewAllUsersComponent },
            { path: 'user/:userId', component: ViewUserByIdComponent },
            { path: 'verify-account', component: UserVerificationApplicationComponent },
            { path: 'account', component: UserAccountManagerComponent },
            { path: 'edit-user/:userId', component: EditUserComponent },
            { path: 'notifications', component: ViewAllNotificationsComponent },
            { path: 'claims', component: ViewAllClaimsComponent },
            { path: 'claims/:userId', component: ViewClaimsByUserIdComponent },
            { path: 'claim/:userId', component: ViewClaimByIdComponent },
            { path: 'temporary-loss-applications', component: ViewAllTemporaryLossApplicationsComponent },
            { path: 'temporary-loss-application/:temporaryLossApplicationId', component: ViewTemporaryLossApplicationByIdComponent },
            { path: 'extract-temporary-loss-application', component: ExtractTemporaryLossApplicationComponent },
            { path: 'capture-temporary-loss-application', component: CameraComponent },
            { path: 'capture-user-document', component: CameraUserIdComponent },
            { path: 'free-text-test', component: FreeTextTestComponent },
        ]
    }
];
