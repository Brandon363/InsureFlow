import { Component, NgZone, OnDestroy, OnInit, signal } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';
import { SharedModules } from './views/shared/shared_modules';
import { Subscription } from 'rxjs';
import { NotificationService } from './services/notification.service';
import { UserService } from './services/user.service';
import { AuthService } from './services/auth.service';
import { MessageService } from 'primeng/api';
import { SharedService } from './services/shared.service';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, SharedModules],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit, OnDestroy {
  private notificationSubscription!: Subscription;
  private initialLoadSubscription!: Subscription;
  private sseSubscription!: Subscription;


  notifications: any[] = [];

  visible: boolean = false;
  title = 'Tender_Board_v1';

  darkMode = signal<boolean>(true);

  darkModeSwitch: boolean = true;
  themeIcon = signal<string>('pi pi-moon')
  authSubscription!: Subscription;
  getAuthSubscription!: Subscription;


  constructor(
    private notificationService: NotificationService,
    // private chatMessageService: ChatMessageService,
    private userService: UserService,
    private authService: AuthService,
    private router: Router,
    private messageService: MessageService,
    private sharedService: SharedService,
    private zone: NgZone
  ) { }

  ngOnInit(): void {
    this.handDarkMode()
    this.getAuthSubscription = this.authService.isAuthenticated().subscribe((reponse)=>{
      if (reponse) {
        this.authService.authStatus.next(true);
      }
    });

    this.getAllActiveUsers();
  }

  // connectToSSE() {
  //   const currentUser = this.authService.getCurrentUser();
  //   if (currentUser) {
  //     this.sseSubscription = this.notificationService.getServerSentEvents().subscribe({
  //       next: (event: any) => {
  //         this.zone.run(() => {
  //           switch (event.event) {
  //             case 'chat_message':
  //               this.handleChatMessage(JSON.parse(event.data) as ChatMessageDTO);
  //               break;
  //             case 'notification':
  //               this.handleNotification(JSON.parse(event.data) as NotificationDTO);
  //               break;
  //             default:
  //               console.warn('Unknown SSE event type:', event);
  //               break;
  //           }
  //         });
  //       },
  //       error: (err) => {
  //         console.error('SSE error:', err);
  //       }
  //     });
  //     this.initialLoadSubscription = this.notificationService.getAllNotificationsByUserId(currentUser.id).subscribe();
  //   }
  // }

  getAllActiveUsers() {
    // this.userService.getAllActiveUsers().subscribe()
  }


  // handleChatMessage(chat_message: ChatMessageDTO) {
  //   // console.log(chat_message)
  //   this.chatMessageService.pushNewMessage(chat_message.workspace_id, chat_message);
  //   this.notificationService.playNewMessageSound();

  //   this.messageService.add({
  //     key: 'newMessageToaster', severity: 'contrast', detail: chat_message.content,
  //     text: '/workspaces'
  //   });
  // }

  // handleNotification(notification: NotificationDTO) {
  //   // console.log(notification)
  //   this.notificationService.playNotificationSound();
  //   this.notificationService.updateUserNotificationData(notification);

  //   this.messageService.add({
  //     key: 'newNotificationToaster', severity: 'contrast', 
  //     detail: this.sharedService.getNotificationDetails(notification).link,
  //     text: this.sharedService.getNotificationDetails(notification).title, 
  //     summary: notification.content, icon: this.sharedService.getNotificationDetails(notification).icon
  //   });
  // }

  handDarkMode() {
    const storedMode = localStorage.getItem('darkMode');

    if (storedMode === null) {
      this.darkMode.set(window.matchMedia('(prefers-color-scheme: dark)').matches);
      localStorage.setItem('darkMode', String(this.darkMode()));
    } else {
      this.darkMode.set(storedMode === 'true');
    }

    const element = document.querySelector('html');

    if (this.darkMode()) {
      element?.classList.add('dark-theme');
      this.themeIcon.set('pi pi-sun');
    } else {
      element?.classList.remove('dark-theme');
      this.themeIcon.set('pi pi-moon');
    }
  }


  ngOnDestroy(): void {
    this.notificationSubscription?.unsubscribe();
    this.initialLoadSubscription?.unsubscribe();
    this.sseSubscription?.unsubscribe();
    this.authSubscription?.unsubscribe();
    this.getAuthSubscription?.unsubscribe();
    this.notificationService.closeSseConnection();
  }

  onOpenNotificationLink(link: string): void {
    this.router.navigateByUrl(link);
    this.messageService.clear('newNotificationToaster');
  }

  onOpenMessageLink(link: string): void {
    // this.router.navigate([link]);
  }

}