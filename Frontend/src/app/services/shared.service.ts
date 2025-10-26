import { Injectable } from '@angular/core';
import { NotificationType } from '../models/enum.interface';
import { NotificationDTO } from '../models/notification.interface';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class SharedService {

  constructor(
    private router: Router
  ) { }

  getNotificationDetails(notification: NotificationDTO): { title: string, icon: string, iconColor: string, link: string } {
    switch (notification.notification_type) {
      case NotificationType.USER_UPDATE:
        return {
          title: notification.title || 'User Update',
          icon: "pi-user",
          iconColor: '#00c950',
          link: '/account'
        };
      case NotificationType.CLAIM_UPDATE:
        return {
          title: notification.title || 'Claim Update',
          icon: "pi-file",
          // iconColor: '#ff0000', 
          iconColor: '#fb2c36',
          link: '/claim/' + notification.claim_id
        };
      case NotificationType.POLICY_UPDATE:
        return {
          title: notification.title || 'Policy Update',
          icon: "pi-shield",
          iconColor: '#00bcff',
          link: '/policy/' + notification.policy_id
        };
      case NotificationType.ANNOUNCEMENT:
        return {
          title: notification.title || 'Announcement',
          icon: "pi-bullhorn",
          iconColor: '#00bcff',
          link: '/'
          // link: '/tenders'
        };
      default:
        return {
          title: 'New notification',
          icon: "pi-bell",
          iconColor: '',
          link: ''
        };
    }
  }

  openNotificationSource(notification: NotificationDTO) {
    const link = this.getNotificationDetails(notification).link
    // console.log(link)
    this.router.navigateByUrl(link)
  }
}
