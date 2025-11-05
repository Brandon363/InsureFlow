import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { UserRole } from '../../../models/enum.interface';
import { UserDTO } from '../../../models/user.interface';
import { VerificationTrackingDTO } from '../../../models/verification_tracking.interface';
import { AuthService } from '../../../services/auth.service';
import { UserService } from '../../../services/user.service';
import { VerificationTrackingService } from '../../../services/verification-tracking.service';
import { SharedModules } from '../../shared/shared_modules';
import { ApplicationTrackingDTO } from '../../../models/application_tracking.interface';
import { TemporaryLossApplicationDTO } from '../../../models/temporary_loss_application.interface';
import { ApplicationTrackingService } from '../../../services/application-tracking.service';

@Component({
  selector: 'app-application-tracking',
  imports: [SharedModules],
  templateUrl: './application-tracking.component.html',
  styleUrl: './application-tracking.component.scss'
})
export class ApplicationTrackingComponent implements OnInit, OnDestroy {
  @Input() temporaryLossApplication!: TemporaryLossApplicationDTO;

  loggedInUser!: UserDTO;

  verificationTrackings: ApplicationTrackingDTO[] = [];
  getAllSubscription!: Subscription;
  getAllUsersSubscription!: Subscription;
  retrieveSubscription!: Subscription;
  users: UserDTO[] = [];



  constructor(
    private applicationTrackingService: ApplicationTrackingService,
    private userService: UserService,
    private authService: AuthService
  ) { }

  ngOnDestroy(): void {
    this.getAllSubscription?.unsubscribe();
    this.retrieveSubscription?.unsubscribe()
    this.getAllUsersSubscription?.unsubscribe()
  }

  events: any[] = [];


  ngOnInit(): void {
    this.loggedInUser = this.authService.getCurrentUser();
    this.getAllSubscription = this.applicationTrackingService.getAllActiveUserVerificationTrackings(this.temporaryLossApplication.id).subscribe()
    this.retrieveSubscription = this.applicationTrackingService.retrieveVerificationTrackingData().subscribe((response) => {
      this.verificationTrackings = response;
      
    })

    if (this.loggedInUser.user_role == UserRole.ADMIN) {
      this.getAllUsersSubscription = this.userService.getAllActiveUsers().subscribe((response) => {
        this.users = response.users!;
      })
    }

  }

  getUserFromId(id: number): string {
    if (!this.users) {
      return '';
    }
    if (!id || id === null || id === undefined) {
      return '';
    }

    else {
      const u = this.users.find(user => user.id === id) as UserDTO;
      if (!u) {
        return '';
      }
      return u.first_name + ' ' + u.last_name;
    }

  }
}
