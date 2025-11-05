import { Component, OnDestroy, OnInit } from '@angular/core';
import { SharedModules } from '../../shared/shared_modules';
import { Router } from '@angular/router';
import { MessageService, ConfirmationService } from 'primeng/api';
import { FileUploadHandlerEvent } from 'primeng/fileupload';
import { Subscription } from 'rxjs';
import { VerificationStatus } from '../../../models/enum.interface';
import { UserDTO } from '../../../models/user.interface';
import { AuthService } from '../../../services/auth.service';
import { ExtractedUserService } from '../../../services/extracted-user.service';
import { LoadingService } from '../../../services/loading.service';
import { NotificationService } from '../../../services/notification.service';
import { ExtractedTemporaryLossApplicationService } from '../../../services/extracted-temporary-loss-application.service';

@Component({
  selector: 'app-extract-temporary-loss-application',
  imports: [SharedModules],
  templateUrl: './extract-temporary-loss-application.component.html',
  styleUrl: './extract-temporary-loss-application.component.scss'
})
export class ExtractTemporaryLossApplicationComponent implements OnInit, OnDestroy {

  verifySubscription!: Subscription;
  user!: UserDTO;

  breadcomb_menu_items = [
    {
      label: 'Home',
      routerLink: '/home-dashboard'
    },
    { label: 'Extract Application' }
  ];
  home = { icon: 'pi pi-home', routerLink: '/client-dashboard' };
  loading = false;

  constructor(
    private messageService: MessageService,
    public loadingService: LoadingService,
    public extractedTemporaryLossService: ExtractedTemporaryLossApplicationService,
    public authService: AuthService,
    private confirmationService: ConfirmationService,
    private router: Router,
    private notificationService: NotificationService) { }

  ngOnDestroy(): void {
    this.verifySubscription?.unsubscribe();
  }

  ngOnInit(): void {
    this.user = this.authService.getCurrentUser();

    // if (this.user.verification_status === VerificationStatus.PENDING) {
    //   this.messageService.add({ severity: 'warn', summary: 'Verification Pending', detail: `You have already submitted verification` })
    //   this.router.navigate(['/client-dashboard']);
    // }

    // if (this.user.verification_status === VerificationStatus.VERIFIED) {
    //   this.messageService.add({ severity: 'info', summary: 'Verified', detail: `Your account is already verified` });
    //   this.router.navigate(['/client-dashboard']);
    // }

    this.loadingService.isManipulatingData$.subscribe((loading) => {
      this.loading = loading;
    });
  }
  uploadedFiles: any[] = [];

  onUpload(event: FileUploadHandlerEvent) {
    this.uploadedFiles = [];
    for (let file of event.files) {
      this.uploadedFiles.push(file);
    }
  }

  // onUpload(event: FileUploadHandlerEvent) {
  //   this.uploadedFiles = this.uploadedFiles || [];
  //   const pdfCount = this.uploadedFiles.filter(file => file === 1).length;
  //   const imageCount = this.uploadedFiles.filter(file => file === 2).length;
  //   const maxPdf = 1;
  //   const maxImages = 2;

  //   for (let file of event.files) {
  //     if (file.type === 'application/pdf' && pdfCount < maxPdf) {
  //       this.uploadedFiles.push(1);
  //     } else if (file.type.startsWith('image/') && imageCount < maxImages) {
  //       this.uploadedFiles.push(2);
  //     } else {
  //       console.error('Maximum file limit reached for this file type');
  //     }
  //   }
  // }

  onClearUploads() {
    this.uploadedFiles = [];
    this.messageService.add({ severity: 'info', summary: 'File Cleared', detail: `All files cleared.` });
  }

  submitVerification() {
    this.loadingService.setLoadingState(true)
    const formData = new FormData();
    this.uploadedFiles.forEach(file => formData.append('files', file));

    this.verifySubscription = this.extractedTemporaryLossService.extractUser(formData, this.user.id).subscribe((response) => {
      this.loadingService.setLoadingState(false)
      if (!response.success) {
        this.messageService.add({ severity: 'error', summary: 'Failed', detail: `${response.message}`, sticky: true })

      } else {
        this.messageService.add({ severity: 'success', summary: 'Submitted', detail: `Appliction extraction successul` })
        if (response.notification) {
          this.notificationService.updateUserNotificationData(response.notification!);
        }
        this.authService.refreshUserData().subscribe(() => {
          this.router.navigate(['/temporary-loss-applications']);
        });


      }
    },
      (error) => {
        console.log(error)
      });
  }

  onRemoveFile(file: any) {
    this.uploadedFiles.splice(this.uploadedFiles.indexOf(file), 1);
    // console.log(this.uploadedFiles);
  }

}
