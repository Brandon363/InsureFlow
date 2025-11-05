import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MessageService, ConfirmationService } from 'primeng/api';
import { AuthService } from '../../../services/auth.service';
import { DocumentService } from '../../../services/document.service';
import { LoadingService } from '../../../services/loading.service';
import { NotificationService } from '../../../services/notification.service';
import { UserService } from '../../../services/user.service';
import { UserDTO } from '../../../models/user.interface';
import { ExtractedTemporaryLossApplicationDTO } from '../../../models/extracted_temporary_loss_application.interface';
import { Subscription } from 'rxjs';
import { TemporaryLossApplicationService } from '../../../services/temporary-loss-application.service';
import { SharedModules } from '../../shared/shared_modules';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { FormArray, FormControl, FormGroup } from '@angular/forms';
import { TemporaryLossApplicationDTO, TemporaryLossApplicationUpdateRequest } from '../../../models/temporary_loss_application.interface';
import { DependentDTO, DependentUpdateRequest } from '../../../models/dependents.interface';
import { ApplicationTrackingComponent } from "../application-tracking/application-tracking.component";
import { ExtractedDependentDTO } from '../../../models/extracted_dependent.interface';
import { ApplicationStage } from '../../../models/enum.interface';

@Component({
  selector: 'app-view-temporary-loss-application-by-id',
  imports: [SharedModules, ApplicationTrackingComponent],
  templateUrl: './view-temporary-loss-application-by-id.component.html',
  styleUrl: './view-temporary-loss-application-by-id.component.scss'
})
export class ViewTemporaryLossApplicationByIdComponent implements OnInit, OnDestroy {

  breadcomb_menu_items = [
    {
      label: 'All Applications',
      routerLink: '/temporary-loss-applications'
    },
    { label: 'Temporary Loss Application Details' }
  ];
  home = { icon: 'pi pi-home', routerLink: '/admin-dashboard' };

  user!: UserDTO;
  extractedApplication!: ExtractedTemporaryLossApplicationDTO;
  pdfUrl!: SafeResourceUrl;
  temporaryLossApplicationId!: number;
  temporaryLossApplication!: TemporaryLossApplicationDTO;

  dependents: DependentDTO[] = []
  extractedDependents: ExtractedDependentDTO[] = []
  combinedDependents: ExtractedDependentDTO[] = []

  getAuthSubscription!: Subscription;
  getSubscription!: Subscription;
  viewDocumentSubscription!: Subscription;
  editSubscription!: Subscription;
  verifyDocumentSubscription!: Subscription;

  editTemporaryLossForm!: FormGroup;

  page: number = 0

  loadingDocument: boolean = false;

  constructor(
    private messageService: MessageService,
    private loadingService: LoadingService,
    private confirmationService: ConfirmationService,
    private router: Router,
    private route: ActivatedRoute,
    private userService: UserService,
    private temporaryLossApplicationService: TemporaryLossApplicationService,
    private authService: AuthService,
    private documentService: DocumentService,
    private notificationService: NotificationService,
    private domSanitizer: DomSanitizer

  ) { }

  ngOnDestroy(): void {
    this.getAuthSubscription?.unsubscribe();
    this.getSubscription?.unsubscribe();
    this.viewDocumentSubscription?.unsubscribe();
    this.editSubscription?.unsubscribe();
    this.verifyDocumentSubscription?.unsubscribe();
    if (this.pdfUrl) {
      const url = this.pdfUrl as string;
      URL.revokeObjectURL(url);
    }
  }

  ngOnInit(): void {
    this.loadingService.setLoadingState(true);

    this.user = this.authService.getCurrentUser();

    const temporaryLossApplicationId = this.route.snapshot.paramMap.get('temporaryLossApplicationId');
    if (temporaryLossApplicationId) {
      this.temporaryLossApplicationId = +temporaryLossApplicationId;
    }

    this.getSubscription = this.temporaryLossApplicationService.getApplicationById(this.temporaryLossApplicationId).subscribe((response) => {
      if (response.success && response.temporaryLossApplication) {
        this.temporaryLossApplication = response.temporaryLossApplication;
        // console.log(this.temporaryLossApplication);
        if (response.temporaryLossApplication.extracted_applications && response.temporaryLossApplication.extracted_applications.length > 0) {
          this.extractedApplication = response.temporaryLossApplication.extracted_applications![response.temporaryLossApplication.extracted_applications!.length - 1];
          // this.comparisons = this.compareFields();
          this.viewDocument(this.temporaryLossApplication.id);
          this.dependents = this.temporaryLossApplication.dependents || [];
          // map to the extracted using ID only to get the confidences 
          this.extractedDependents = this.extractedApplication.extracted_dependents || [];
          this.combinedDependents = this.mapDependents();
          // console.log(d)

        }

        this.initializeForm()
      }
      this.loadingService.setLoadingState(false);

    });


  }

  initializeForm() {
    this.editTemporaryLossForm = new FormGroup({
      id: new FormControl(this.temporaryLossApplication.id),
      extracted_application_id: new FormControl(this.temporaryLossApplication.extracted_application_id),
      full_name: new FormControl(this.temporaryLossApplication.full_name),
      id_number: new FormControl(this.temporaryLossApplication.id_number),
      date_of_birth: new FormControl(this.temporaryLossApplication.date_of_birth),
      contact_number: new FormControl(this.temporaryLossApplication.contact_number),
      email: new FormControl(this.temporaryLossApplication.email),
      address: new FormControl(this.temporaryLossApplication.address),
      nok_full_name: new FormControl(this.temporaryLossApplication.nok_full_name),
      nok_contact_number: new FormControl(this.temporaryLossApplication.nok_contact_number),
      bank_name: new FormControl(this.temporaryLossApplication.bank_name),
      account_number: new FormControl(this.temporaryLossApplication.account_number),
      branch_code: new FormControl(this.temporaryLossApplication.branch_code),
      existing_insurance_with_other_company: new FormControl(this.temporaryLossApplication.existing_insurance_with_other_company),
      existing_chronic_condition: new FormControl(this.temporaryLossApplication.existing_chronic_condition),
      status: new FormControl(this.temporaryLossApplication.status),
      agent_full_name: new FormControl(this.temporaryLossApplication.agent_full_name),
      agent_number: new FormControl(this.temporaryLossApplication.agent_number),
      title: new FormControl(this.temporaryLossApplication.title),
      gender: new FormControl(this.temporaryLossApplication.gender),
      b_date_of_birth: new FormControl(this.temporaryLossApplication.b_date_of_birth),
      claim_ailment: new FormControl(this.temporaryLossApplication.claim_ailment),
      claim_amount: new FormControl(this.temporaryLossApplication.claim_amount),
      declined_coverage: new FormControl(this.temporaryLossApplication.declined_coverage),
      declined_cover_reason: new FormControl(this.temporaryLossApplication.declined_cover_reason),
      // dependents: new FormArray((this.temporaryLossApplication.dependents || []).map(dependent => this.createDependentFormGroup(dependent)))
      dependents: new FormArray((this.temporaryLossApplication!.dependents || []).map(dependent => this.createDependentFormGroup(dependent)))
    });
  }

  mapDependents(): any[] {
    const result: any[] = this.dependents.map((dependent: DependentDTO) => {
      const extracted: ExtractedDependentDTO | undefined = this.extractedDependents.find(
        e => e.dependant_id === dependent.id
      );

      return {
        id: dependent.id,
        application_id: dependent.application_id,
        full_name: dependent.full_name,
        full_name_confidence: extracted?.full_name_confidence ?? null,
        id_number: dependent.id_number,
        id_number_confidence: extracted?.id_number_confidence ?? null,
        date_of_birth: dependent.date_of_birth,
        date_of_birth_confidence: extracted?.date_of_birth_confidence ?? null,
        age: dependent.age,
        age_confidence: extracted?.age_confidence ?? null,
        gender: dependent.gender,
        gender_confidence: extracted?.gender_confidence ?? null,
        client_relationship: dependent.client_relationship,
        client_relationship_confidence: extracted?.client_relationship_confidence ?? null,
        entity_status: extracted?.entity_status ?? null,
        date_created: dependent.date_created ?? extracted?.date_created ?? null,
        date_updated: dependent.date_updated ?? extracted?.date_updated ?? null,
      };
    });

    return result;
  }


  createDependentFormGroup(dependent: any): FormGroup {
    return new FormGroup({
      id: new FormControl(dependent.id),
      full_name: new FormControl(dependent.full_name),
      id_number: new FormControl(dependent.id_number),
      date_of_birth: new FormControl(dependent.date_of_birth),
      age: new FormControl(dependent.age),
      gender: new FormControl(dependent.gender),
      client_relationship: new FormControl(dependent.client_relationship),
    });
  }


  viewDocument(user_id: number): void {
    this.loadingDocument = true;
    this.loadingService.setLoadingState(true);
    this.viewDocumentSubscription = this.documentService.getApplicationDocumentFileByTemporaryLossApplicationId(user_id).subscribe({
      next: pdfBlob => {
        this.loadingDocument = false;
        this.loadingService.setLoadingState(false);
        const url = URL.createObjectURL(pdfBlob);
        this.pdfUrl = this.domSanitizer.bypassSecurityTrustResourceUrl(url);
      },
      error: error => {
        this.loadingDocument = false;
        this.loadingService.setLoadingState(false);
        console.error(error);
      }
    });
  }

  onPageChange(a: any) {
    // console.log(a);
    this.page = a.page

  }


  getValueAndSeverityFromConfidence(confidence: number | undefined) {
    if (confidence === undefined) {
      return { severity: 'info' as const, value: 'N/A' };
    }
    const percent = parseFloat((confidence * 100).toFixed(2));
    switch (true) {
      case percent >= 80:
        return { severity: 'success' as const, value: `${percent}%` };

      case percent >= 50:
        return { severity: 'info' as const, value: `${percent}%` };

      case percent >= 30:
        return { severity: 'warn' as const, value: `${percent}%` };

      case percent >= 0:
        return { severity: 'danger' as const, value: `${percent}%` };

      default:
        return { severity: 'info' as const, value: `${percent}%` };
    }
  }


  onSubmit() {
    this.loadingService.setLoadingState(true);
    const temporaryLossApplicationUpdateRequest: TemporaryLossApplicationUpdateRequest = this.editTemporaryLossForm.value;
    const dependentsUpdateRequest: DependentUpdateRequest[] = this.combinedDependents.map(dependent => {
      return {
        id: dependent.id,
        application_id: this.temporaryLossApplication.id,
        full_name: dependent.full_name,
        id_number: dependent.id_number,
        date_of_birth: dependent.date_of_birth,
        age: dependent.age,
        gender: dependent.gender,
        client_relationship: dependent.client_relationship,
      };
    });
    temporaryLossApplicationUpdateRequest.dependents = dependentsUpdateRequest;
    this.editSubscription = this.temporaryLossApplicationService.editApplicationAndDependents(this.temporaryLossApplication.id, temporaryLossApplicationUpdateRequest).subscribe((response) => {
      this.loadingService.setLoadingState(false);
      if (!response.success) {
        this.loadingService.setLoadingState(false);
        this.messageService.add({
          severity: 'error',
          summary: 'Edit Failed',
          detail: response.message
        });
        return;
      }

      this.messageService.add({ severity: 'success', summary: 'Edit Successful', detail: response.message });
      // this.router.navigate(['/account']);
    })

  }

  onClickSubmit() {
    this.confirmationService.confirm({
      message: 'Proceed with update?',
      header: 'Confirmation',
      icon: 'pi pi-info-circle',
      acceptButtonProps: {
        label: 'Yes',
        severity: 'primary',
      },
      rejectButtonProps: {
        label: 'Cancel',
        severity: 'secondary',
        outlined: true
      },
      accept: () => {
        this.onSubmit()
      },
      reject: () => {
      }
    });
  }

  onClickVerify() {
    this.confirmationService.confirm({
      message: 'Proceed with verification?',
      header: 'Confirmation',
      icon: 'pi pi-info-circle',
      acceptButtonProps: {
        label: 'Yes',
        severity: 'primary',
      },
      rejectButtonProps: {
        label: 'Cancel',
        severity: 'secondary',
        outlined: true
      },
      accept: () => {
        this.onVerify()
      },
      reject: () => {
      }
    });
  }


  onVerify() {
    this.loadingService.setLoadingState(true);
    this.editSubscription = this.temporaryLossApplicationService.verifyDocuments(this.temporaryLossApplication.id, this.user.id).subscribe((response) => {
      this.loadingService.setLoadingState(false);
      if (!response.success) {
        this.loadingService.setLoadingState(false);
        this.messageService.add({
          severity: 'error',
          summary: 'Verification Failed',
          detail: response.message
        });
        return;
      }
      this.temporaryLossApplication = response.temporaryLossApplication!;
      this.messageService.add({ severity: 'success', summary: 'Verification Successful', detail: response.message });
      // this.router.navigate(['/account']);
    })

  }

  showVerifyButton(): boolean {
    if (this.temporaryLossApplication) {
      const tracks = this.temporaryLossApplication.application_tracking_stages;
      if (tracks && tracks.length > 0) {
        const lastTrack = tracks[tracks.length - 1];
        const appStatus = lastTrack.stage

        if (appStatus == ApplicationStage.SUBMITTED) {
          return true;
        }
      }
    }
    // else {
    return false;
    // }
  }


}
