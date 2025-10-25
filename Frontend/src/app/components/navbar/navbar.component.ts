import { Component, OnDestroy, OnInit } from '@angular/core';
import { Router, RouterOutlet } from "@angular/router";
import { SharedModules } from '../../views/shared/shared_modules';
import { MenuItem, MessageService } from 'primeng/api';
import { Subscription } from 'rxjs';
import { LoadingService } from '../../services/loading.service';
import { NotificationService } from '../../services/notification.service';
import { AuthService } from '../../services/auth.service';
import { SharedService } from '../../services/shared.service';
import { AppComponent } from '../../app.component';
import { NotificationDTO } from '../../models/notification.interface';
import { UserRole } from '../../models/enum.interface';

@Component({
  selector: 'app-navbar',
  imports: [RouterOutlet, SharedModules],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.scss'
})
export class NavbarComponent implements OnInit, OnDestroy {
  items: MenuItem[] | undefined;
  isManipulatingData: boolean = false;
  loadingSubscription!: Subscription;
  // darkMode: boolean = true;
  themeIcon: string = 'pi pi-moon'
  username: string = "-"
  avatarText: string = "-";

  workspacesWithUnread: number = 0;

  notificationSubscription!: Subscription;
  logoutSubscription!: Subscription;

  allActiveNotifications!: NotificationDTO[];
  allActiveUnreadNotifications: NotificationDTO[] = [];

  constructor(
    private router: Router,
    private loadingService: LoadingService,
    private notificationService: NotificationService,
    // private workspaceService: WorkspaceService,
    private authService: AuthService,
    private messageService: MessageService,
    private sharedService: SharedService,
    private app: AppComponent
  ) { }


  ngOnInit() {
    const user = this.authService.getCurrentUser();
    const firstName = user.first_name ?? "-";
    const lastName = user.last_name ?? "-";

    this.notificationSubscription = this.notificationService.allActiveUserNotifications.subscribe((notifications) => {
      this.allActiveNotifications = notifications;

      if (user.user_role === UserRole.CUSTOMER) {

        this.items = [
          {
            label: "Home",
            icon: 'pi pi-fw pi-home',
            routerLink: "/client-dashboard",
          },
          {
            label: "My Claims",
            icon: 'pi pi-fw pi-money-bill',
            routerLink: "/claims",
          },
          {
            label: "Notifications",
            icon: 'pi pi-fw pi-bell',
            badge: this.allActiveUnreadNotifications.length.toString(),
            routerLink: "/notifications",
          },
          {
            label: 'My Account',
            icon: 'pi pi-cog',
            routerLink: '/settings'
          },
          {
            label: 'Logout',
            icon: 'pi pi-sign-out',
            command: () => {
              this.onLogout();
            }
          }
        ]
      } else {
        this.items = [
          {
            label: "Home",
            icon: 'pi pi-fw pi-home',
            routerLink: "/admin-dashboard",
          },
          {
            label: "Clients",
            icon: 'pi pi-fw pi-users',
            routerLink: "/clients",
          },
          {
            label: "Claims",
            icon: 'pi pi-fw pi-money-bill',
            routerLink: "/claims",
          },
          {
            label: "Documents",
            icon: 'pi pi-fw pi-file-pdf',
            routerLink: "/documents",
            badge: this.workspacesWithUnread.toString(),
          },
          {
            label: "Notifications",
            icon: 'pi pi-fw pi-bell',
            badge: this.allActiveUnreadNotifications.length.toString(),
            routerLink: "/notifications",
          },
          {
            label: 'Settings',
            icon: 'pi pi-cog',
            routerLink: '/settings'
          },
          {
            label: 'Logout',
            icon: 'pi pi-sign-out',
            command: () => {
              this.onLogout();
            }
          }
        ];
      }
    });


    this.avatarText = `${firstName.charAt(0).toUpperCase()}${lastName.charAt(0).toUpperCase()}`;
    this.loadingSubscription = this.loadingService.isManipulatingData$.subscribe((isLoading) => {
      Promise.resolve(null).then(() => {
        this.isManipulatingData = isLoading;
      });
    });

  }


  onLogout() {
    this.loadingService.setLoadingState(true);
    this.logoutSubscription = this.authService.logout().subscribe((response) => {
      this.loadingService.setLoadingState(false);
      if (!response.success) {
        this.messageService.add({ severity: 'error', summary: 'Logout Failed', detail: response.message });
        return;
      }

      this.messageService.add({ severity: 'success', summary: 'Logged Out', detail: `You have been logged out successfully.` });
      this.router.navigate(['/login']);
    })
  }

  ngOnDestroy(): void {
    this.loadingSubscription?.unsubscribe();
    this.logoutSubscription?.unsubscribe();
  }

  darkModeSwitch: boolean = true

  toggleDarkMode() {
    this.app.darkMode.set(!this.app.darkMode());
    localStorage.setItem('darkMode', String(this.app.darkMode()));

    const element = document.querySelector('html');

    if (this.app.darkMode()) {
      element?.classList.add('dark-theme');
      this.themeIcon = 'pi pi-sun';
    } else {
      element?.classList.remove('dark-theme');
      this.themeIcon = 'pi pi-moon';
    }
  }


  // toggleDarkMode() {
  // toggleDarkMode() {
  //   this.darkMode = !this.darkMode;
  //   localStorage.setItem('darkMode', String(this.darkMode));

  //   const element = document.querySelector('html');

  //   if (this.darkMode) {
  //     element?.classList.add('dark-theme');
  //     // usePreset(Lara);
  //     this.themeIcon = 'pi pi-sun';
  //   } else {
  //     element?.classList.remove('dark-theme');
  //     // usePreset(MyPreset);
  //     this.themeIcon = 'pi pi-moon';
  //   }
  // }

  isActiveMenu(path: string): boolean {
    const url = this.router.url;

    if (path === '/clients') {
      return url.startsWith('/clients') || url.startsWith('/user') || url.startsWith('/edit-user') || url.startsWith('/add-tender') || url.startsWith('/chat-with-tender');
    }
    if (path === '/settings') {
      return url.startsWith('/account') || url.startsWith('/verify') || url.startsWith('/create-proposal') || url.startsWith('/edit-proposal');
    }

    // Default match
    return url.startsWith(path);
  }
}