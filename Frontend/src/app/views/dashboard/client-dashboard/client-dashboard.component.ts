import { Component, OnDestroy, OnInit } from '@angular/core';
import { SharedModules } from '../../shared/shared_modules';
import { Router } from '@angular/router';
import { MessageService, ConfirmationService } from 'primeng/api';
import { Table } from 'primeng/table';
import { Subscription } from 'rxjs';
import { ClaimStatus, VerificationStatus } from '../../../models/enum.interface';
import { LoadingService } from '../../../services/loading.service';
import { UserService } from '../../../services/user.service';
import { AuthService } from '../../../services/auth.service';
import { ClaimService } from '../../../services/claim.service';
import { ClaimDTO } from '../../../models/claim.interface';
import { UserDTO } from '../../../models/user.interface';

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


  allClaims: ClaimDTO[] = [];

  statusSelected: string = '';
  selectedUser: ClaimDTO | undefined;


  showAddUserDialog: boolean = false;
  showEditUserDialog: boolean = false;

  reviewStatuses = [
    { label: 'Pending Review', value: null },
    { label: 'Confirmed Fraud', value: 1 },
    { label: 'Dismissed', value: 0 }
  ];

  constructor(
    private claimService: ClaimService,
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
    this.getAllClaims();
  }

  addTestConfig() {
    this.showAddUserDialog = true;
  }

  getAllClaims() {
    this.loadingService.setLoadingState(true);
    this.loading = true;
    this.getAllSubscription = this.claimService.getAllActiveUserClaims(this.user.id).subscribe()
    this.retrieveSubscription = this.claimService.retrieveClaimData().subscribe((response) => {
      console.log(response);
      this.allClaims = response;
      this.allClaims = response.sort((a, b) => {
        const dateA = a.date_updated ? new Date(a.date_updated).getTime() : 0;
        const dateB = b.date_updated ? new Date(b.date_updated).getTime() : 0;
        return dateB - dateA;
      });

      this.updateCardNumbers(null);
      this.loadingService.setLoadingState(false);
      this.loading = false;
    })
  }


  onDeleteClaim(productBufferLevel: ClaimDTO) {
    if (productBufferLevel.id) {
      this.loadingService.setLoadingState(true);
      this.deleteSubscription = this.claimService.deleteClaimById(productBufferLevel.id).subscribe((response) => {
        this.loadingService.setLoadingState(false);
        if (response.success) {
          this.messageService.add({ severity: 'success', summary: 'Success', detail: `${response.message}` })
        } else {
          this.messageService.add({ severity: 'error', summary: 'Failed', detail: `${response.message}` })
        }
      })
    }

  }


  confirmDelete(event: Event, productBufferLevel: ClaimDTO) {
    this.confirmationService.confirm({
      target: event.target as EventTarget,
      message: 'Do you want to delete this claim?',
      header: 'Delete Claim',
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
        this.onDeleteClaim(productBufferLevel);
      },
      reject: () => {
      },
    });
  }


  clear(table: Table) {
    table.clear();
  }


  getStatusSeverityAndWord(status: ClaimStatus) {
    switch (status) {
      case status = ClaimStatus.REJECTED:
        return { severity: 'danger' as const, status: 'Rejected' };

      case status = ClaimStatus.SUBMITTED:
        return { severity: 'info' as const, status: 'Submitted' };

      case status = ClaimStatus.IN_REVIEW:
        return { severity: 'secondary' as const, status: 'Pending' };

      case status = ClaimStatus.APPROVED:
        return { severity: 'success' as const, status: 'Verified' };

      case status = ClaimStatus.PAID:
        return { severity: 'success' as const, status: 'Paid' };

      default:
        return { severity: 'info' as const, status: 'Unknown' };
    }
  }


  updateCardNumbers(dt: any) {
    this.cards = [
      {
        title: "Total Clients",
        value: this.allClaims.length.toString(),
        description: "Active clients in the system",
        icon: "pi pi-money-bill"
      },
      {
        title: "Approved Claims",
        value: this.allClaims.filter(c => c.status === ClaimStatus.APPROVED).length.toString(),
        description: "Verified clients in the system",
        icon: "pi pi-verified"
      },
      {
        title: "In Review Claims",
        value: this.allClaims.filter(c => c.status === ClaimStatus.IN_REVIEW).length.toString(),
        description: "In review claims in the system",
        icon: "pi pi-clock"
      },
      {
        title: "Rejected Claims",
        value: this.allClaims.filter(c => c.status === ClaimStatus.REJECTED).length.toString(),
        description: "Rejected claims in the system",
        icon: "pi pi-times-circle"
      }
    ]
  }


  viewUserDetails(user: ClaimDTO) {
    this.router.navigate(['/claim/', user.id]);
  }

}
