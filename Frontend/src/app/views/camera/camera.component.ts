import { HttpClient } from '@angular/common/http';
import { Component, HostListener, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { Subject, Subscription } from 'rxjs';
import { SharedModules } from '../shared/shared_modules';
import { WebcamImage, WebcamInitError, WebcamUtil } from 'ngx-webcam';
import { environment } from '../../../environments/environment.development';
import { ConfirmationService, MessageService } from 'primeng/api';
import { AuthService } from '../../services/auth.service';
import { ExtractedTemporaryLossApplicationService } from '../../services/extracted-temporary-loss-application.service';
import { LoadingService } from '../../services/loading.service';
import { NotificationService } from '../../services/notification.service';
import { Router } from '@angular/router';
import { UserDTO } from '../../models/user.interface';

@Component({
  selector: 'app-camera',
  imports: [SharedModules],
  templateUrl: './camera.component.html',
  styleUrl: './camera.component.scss'
})
export class CameraComponent implements OnInit, OnDestroy {

  @ViewChild('webcam') webcam: any;

  trigger: Subject<void> = new Subject<void>();
  images: WebcamImage[] = [];

  verifySubscription!: Subscription;
  user!: UserDTO;


  breadcomb_menu_items = [
    {
      label: 'All Applications',
      routerLink: '/temporary-loss-applications'
    },
    { label: 'Capture Application' }
  ];
  home = { icon: 'pi pi-home', routerLink: '/admin-dashboard' };

  constructor(
    public messageService: MessageService,
    private http: HttpClient,
    private loadingService: LoadingService,
    private extractedTemporaryLossService: ExtractedTemporaryLossApplicationService,
    private authService: AuthService,
    private confirmationService: ConfirmationService,
    private router: Router,
    private notificationService: NotificationService) { }


  ngOnDestroy(): void {
    this.verifySubscription?.unsubscribe();
  }

  ngOnInit(): void {
    this.user = this.authService.getCurrentUser();
    // throw new Error('Method not implemented.');
  }

  triggerSnapshot(): void {
    this.trigger.next();
  }

  responseData: any;
  isLoading = false;

  handleImage(webcamImage: WebcamImage): void {
    this.images.push(webcamImage);
    // this.uploadImage();
  }

  removeImage(index: number): void {
    this.images.splice(index, 1);
    // this.previewImages.splice(index, 1);
  }


  uploadImage() {
    this.loadingService.setLoadingState(true)
    const formData = new FormData();
    this.images.forEach((image, index) => {
      this.dataURLtoBlob(image.imageAsDataUrl).then(blob => {
        const file = new File([blob], `image${index}.jpg`, { type: 'image/jpeg' });
        formData.append('files', file);
        if (index === this.images.length - 1) {
          this.uploadForm(formData);
        }
      });
    });
  }



  uploadForm(formData: FormData) {
    this.verifySubscription = this.extractedTemporaryLossService.extractUser(formData, this.user.id).subscribe((response) => {
      this.loadingService.setLoadingState(false)
      if (!response.success) {
        this.messageService.add({ severity: 'error', summary: 'Failed', detail: `${response.message}`, sticky: true })
      } else {
        this.messageService.add({ severity: 'success', summary: 'Submitted', detail: `Application extraction successful` })
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

  async dataURLtoBlob(dataurl: string): Promise<Blob> {
    const response = await fetch(dataurl);
    return response.blob();
  }

  handleInitError(error: WebcamInitError): void {
    if (error.mediaStreamError && error.mediaStreamError.name === "NotAllowedError") {
      console.warn("Camera access was not allowed by user!");
      this.messageService.add({ severity: 'error', summary: 'Camera Access Denied', detail: 'Please allow camera access to use this feature.' });
    }
  }


  @HostListener('document:keydown.enter', ['$event'])
  handleGlobalEnter() {
    if (this.images.length >= 2) {
      return
    }
    else {
      return this.triggerSnapshot()
    }
  }

  width = window.innerWidth < 768 ? 280 : 800;

}
