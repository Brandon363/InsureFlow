import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { UserDTO } from '../../../models/user.interface';
import { TemporaryLossApplicationDTO } from '../../../models/temporary_loss_application.interface';
import { TemporaryLossApplicationService } from '../../../services/temporary-loss-application.service';
import { LoadingService } from '../../../services/loading.service';
import { ConfirmationService, MessageService } from 'primeng/api';
import { Router } from '@angular/router';
import { AuthService } from '../../../services/auth.service';
import { ApplicationStatus, VerificationStatus } from '../../../models/enum.interface';
import { Table } from 'primeng/table';
import { SharedModules } from '../../shared/shared_modules';

@Component({
  selector: 'app-view-all-temporary-loss-applications',
  imports: [SharedModules],
  templateUrl: './view-all-temporary-loss-applications.component.html',
  styleUrl: './view-all-temporary-loss-applications.component.scss'
})
export class ViewAllTemporaryLossApplicationsComponent implements OnInit, OnDestroy {

  getAllSubscription!: Subscription;
  retrieveSubscription!: Subscription;
  editSubscription!: Subscription;
  deleteSubscription!: Subscription;
  loadingSubscription!: Subscription;
  downloadEmptyBufferLevelsSubscription!: Subscription;
  downloadTemplateSubscription!: Subscription;
  syncSubscription!: Subscription;

  user: UserDTO = {} as UserDTO;


  allProductBufferLevels: TemporaryLossApplicationDTO[] = [];

  statusSelected: string = '';
  selectedProductBufferLevel: TemporaryLossApplicationDTO | undefined;


  showAddConfigDialog: boolean = false;
  showEditProductBufferLevelDialog: boolean = false;

  reviewStatuses = [
    { label: 'Pending Review', value: null },
    { label: 'Confirmed Fraud', value: 1 },
    { label: 'Dismissed', value: 0 }
  ];

  constructor(
    private productBufferLevelService: TemporaryLossApplicationService,
    private loadingService: LoadingService,
    private messageService: MessageService,
    private router: Router,
    private authService: AuthService,
    private confirmationService: ConfirmationService) { }

  cards: any[] = [];
  loading = true;
  uploadedFiles: any[] = [];

  verificationStatus = VerificationStatus;


  ngOnDestroy(): void {
    this.getAllSubscription?.unsubscribe();
    this.retrieveSubscription?.unsubscribe();
    this.editSubscription?.unsubscribe();
    this.deleteSubscription?.unsubscribe();
    this.loadingSubscription?.unsubscribe();
    this.downloadEmptyBufferLevelsSubscription?.unsubscribe();
    this.downloadTemplateSubscription?.unsubscribe();
    this.syncSubscription?.unsubscribe();
  }

  ngOnInit(): void {
    this.user = this.authService.getCurrentUser();
    this.getAllTestConfigs();
  }

  addTestConfig() {
    this.showAddConfigDialog = true;
  }

  getAllTestConfigs() {
    this.loadingService.setLoadingState(true);
    this.loading = true;
    this.getAllSubscription = this.productBufferLevelService.getAllActiveApplications().subscribe();
    this.retrieveSubscription = this.productBufferLevelService.retrieveApplicationData().subscribe((response) => {
      console.log(response);
      this.allProductBufferLevels = response;
      this.allProductBufferLevels = response.sort((a, b) => {
        const dateA = a.date_updated ? new Date(a.date_updated).getTime() : 0;
        const dateB = b.date_updated ? new Date(b.date_updated).getTime() : 0;
        return dateB - dateA;
      });

      this.updateCardNumbers(null);
      this.loadingService.setLoadingState(false);
      this.loading = false;
    })
  }


  // viewProductBufferLevel(productBufferLevel: UserDTO) {
  //   if (productBufferLevel) {
  //     this.selectedProductBufferLevel = productBufferLevel;
  //     this.showEditProductBufferLevelDialog = true;
  //   }
  // }


  onDeleteProductBufferLevel(productBufferLevel: UserDTO) {
    if (productBufferLevel.id) {
      this.loadingService.setLoadingState(true);
      this.deleteSubscription = this.productBufferLevelService.deleteApplicationById(productBufferLevel.id).subscribe((response) => {
        this.loadingService.setLoadingState(false);
        if (response.success) {
          this.messageService.add({ severity: 'success', summary: 'Success', detail: `${response.message}` })
        } else {
          this.messageService.add({ severity: 'error', summary: 'Failed', detail: `${response.message}` })
        }
      })
    }

  }


  confirmDelete(event: Event, productBufferLevel: UserDTO) {
    this.confirmationService.confirm({
      target: event.target as EventTarget,
      message: 'Do you want to delete this application?',
      header: 'Delete Application',
      icon: 'pi pi-info-circle',
      rejectLabel: 'Cancel',
      rejectButtonProps: {
        label: 'Cancel',
        severity: 'secondary',
        outlined: true,
      },
      acceptButtonProps: {
        label: 'Delete',
        severity: 'danger',
      },

      accept: () => {
        this.onDeleteProductBufferLevel(productBufferLevel);
      },
      reject: () => {
      },
    });
  }


  clear(table: Table) {
    table.clear();
  }


  getStatusSeverityAndWord(status: ApplicationStatus) {
    switch (status) {
      case status = ApplicationStatus.DECLINED:
        return { severity: 'danger' as const, status: 'Rejected' };

      case status = ApplicationStatus.IN_PROGRESS:
        return { severity: 'danger' as const, status: 'In Progress' };

      case status = ApplicationStatus.PENDING:
        return { severity: 'warn' as const, status: 'Pending' };

      case status = ApplicationStatus.APPROVED:
        return { severity: 'success' as const, status: 'Verified' };

      default:
        return { severity: 'info' as const, status: 'Unknown' };
    }
  }


  updateCardNumbers(dt: any) {
    this.cards = [
      {
        title: "Total Applications",
        value: this.allProductBufferLevels.length.toString(),
        description: "Active applications in the system",
        icon: "pi pi-users"
      },
      {
        title: "Approved Applications",
        value: this.allProductBufferLevels.filter(c => c.status === ApplicationStatus.APPROVED).length.toString(),
        description: "Approved applications in the system",
        icon: "pi pi-verified"
      },
      {
        title: "Pending Applications",
        value: this.allProductBufferLevels.filter(c => c.status === ApplicationStatus.PENDING).length.toString(),
        description: "Pending applications in the system",
        icon: "pi pi-clock"
      },
      {
        title: "In Progress Applications",
        //Clients",
        value: this.allProductBufferLevels.filter(c => c.status === ApplicationStatus.IN_PROGRESS).length.toString(),
        description: "Applications in the system in progress",
        icon: "pi pi-clock"
      }
    ]
  }


  viewUserDetails(temporaryApplication: TemporaryLossApplicationDTO) {
    this.router.navigate(['/temporary-loss-application/', temporaryApplication.id]);
  }

}
