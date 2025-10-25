import { Component, OnDestroy, OnInit } from '@angular/core';
import { SharedModules } from '../../shared/shared_modules';
import { Router } from '@angular/router';
import { MessageService, ConfirmationService } from 'primeng/api';
import { Table } from 'primeng/table';
import { Subscription } from 'rxjs';
import { VerificationStatus } from '../../../models/enum.interface';
import { UserDTO } from '../../../models/user.interface';
import { LoadingService } from '../../../services/loading.service';
import { UserService } from '../../../services/user.service';
import { AuthService } from '../../../services/auth.service';

@Component({
  selector: 'app-client-dashboard',
  imports: [SharedModules],
  templateUrl: './client-dashboard.component.html',
  styleUrl: './client-dashboard.component.scss'
})
export class ClientDashboardComponent implements OnInit, OnDestroy {

  getAllSubscription!: Subscription;
  retrieveSubscription!: Subscription;
  editSubscription!: Subscription;
  deleteSubscription!: Subscription;
  loadingSubscription!: Subscription;
  downloadEmptyBufferLevelsSubscription!: Subscription;
  downloadTemplateSubscription!: Subscription;
  syncSubscription!: Subscription;

  user: UserDTO = {} as UserDTO;


  allProductBufferLevels: UserDTO[] = [];

  statusSelected: string = '';
  selectedProductBufferLevel: UserDTO | undefined;


  showAddConfigDialog: boolean = false;
  showEditProductBufferLevelDialog: boolean = false;

  reviewStatuses = [
    { label: 'Pending Review', value: null },
    { label: 'Confirmed Fraud', value: 1 },
    { label: 'Dismissed', value: 0 }
  ];

  constructor(
    private productBufferLevelService: UserService,
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
    this.getAllSubscription = this.productBufferLevelService.getAllActiveUsers().subscribe()
    this.retrieveSubscription = this.productBufferLevelService.retrieveUserData().subscribe((response) => {
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
      this.deleteSubscription = this.productBufferLevelService.deleteUserById(productBufferLevel.id).subscribe((response) => {
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
      message: 'Do you want to delete this client?',
      header: 'Delete Buffer Level',
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


  getStatusSeverityAndWord(status: VerificationStatus) {
    switch (status) {
      case status = VerificationStatus.REJECTED:
        return { severity: 'danger' as const, status: 'Rejected' };

      case status = VerificationStatus.UNVERIFIED:
        return { severity: 'danger' as const, status: 'Unverified' };

      case status = VerificationStatus.PENDING:
        return { severity: 'warn' as const, status: 'Pending' };

      case status = VerificationStatus.VERIFIED:
        return { severity: 'success' as const, status: 'Verified' };

      default:
        return { severity: 'info' as const, status: 'Unknown' };
    }
  }


  updateCardNumbers(dt: any) {
    this.cards = [
      {
        title: "Total Clients",
        value: this.allProductBufferLevels.length.toString(),
        description: "Active clients in the system",
        icon: "pi pi-users"
      },
      {
        title: "Verified Clients",
        value: this.allProductBufferLevels.filter(c => c.verification_status === VerificationStatus.VERIFIED).length.toString(),
        description: "Verified clients in the system",
        icon: "pi pi-verified"
      },
      {
        title: "Pending Verification",
        value: this.allProductBufferLevels.filter(c => c.verification_status === VerificationStatus.PENDING).length.toString(),
        description: "Unverified clients in the system",
        icon: "pi pi-clock"
      },
      {
        title: "Unverified Clients",
        value: this.allProductBufferLevels.filter(c => c.verification_status === VerificationStatus.UNVERIFIED).length.toString(),
        description: "Unverified clients in the system",
        icon: "pi pi-clock"
      }
    ]
  }


  viewUserDetails(user: UserDTO) {
    this.router.navigate(['/user/', user.id]);
  }

}
