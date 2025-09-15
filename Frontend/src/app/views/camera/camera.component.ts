import { HttpClient } from '@angular/common/http';
import { Component, ViewChild } from '@angular/core';
import { Subject } from 'rxjs';
import { SharedModules } from '../shared/shared_modules';
import { WebcamImage, WebcamInitError, WebcamUtil } from 'ngx-webcam';
import { environment } from '../../../environments/environment.development';
import { MessageService } from 'primeng/api';

@Component({
  selector: 'app-camera',
  imports: [SharedModules],
  templateUrl: './camera.component.html',
  styleUrl: './camera.component.scss'
})
export class CameraComponent {

  @ViewChild('webcam') webcam: any;

  trigger: Subject<void> = new Subject<void>();
  image: WebcamImage | null = null;

  constructor(private http: HttpClient, public messageService: MessageService) { }

  triggerSnapshot(): void {
    this.trigger.next();
  }

  responseData: any;
  isLoading = false;

  handleImage(webcamImage: WebcamImage): void {
    this.image = webcamImage;
    this.uploadImage();
  }

  uploadImage(): void {
    if (this.image) {
      this.isLoading = true;
      const imageData = this.image.imageAsDataUrl;
      this.dataURLtoBlob(imageData).then(blob => {
        const formData = new FormData();
        formData.append('image', blob);
        this.http.post(`${environment.baseUrl}/upload`, formData)
          .subscribe((response) => {
            this.isLoading = false;
            this.responseData = response;
            console.log(response);
          });
      });
    }
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

}
