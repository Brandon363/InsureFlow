import { Component, OnDestroy, OnInit } from '@angular/core';
import { SharedModules } from '../../shared/shared_modules';
import { Subscription } from 'rxjs';
import { UserDTO } from '../../../models/user.interface';
import { UserService } from '../../../services/user.service';
import { LoadingService } from '../../../services/loading.service';
import { ConfirmationService, MessageService } from 'primeng/api';
import { Table } from 'primeng/table';

@Component({
  selector: 'app-view-all-users',
  imports: [SharedModules],
  templateUrl: './view-all-users.component.html',
  styleUrl: './view-all-users.component.scss'
})
export class ViewAllUsersComponent implements OnInit, OnDestroy {

  getAllSubscription!: Subscription;
  retrieveSubscription!: Subscription;
  editSubscription!: Subscription;
  deleteSubscription!: Subscription;
  loadingSubscription!: Subscription;
  downloadEmptyBufferLevelsSubscription!: Subscription;
  downloadTemplateSubscription!: Subscription;
  syncSubscription!: Subscription;


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
    private confirmationService: ConfirmationService) { }

  cards: any[] = [];
  loading = true;
  uploadedFiles: any[] = [];


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

      this.allProductBufferLevels = response;
      this.allProductBufferLevels = response.sort((a, b) => {
        const dateA = a.date_updated ? new Date(a.date_updated).getTime() : 0;
        const dateB = b.date_updated ? new Date(b.date_updated).getTime() : 0;
        return dateB - dateA;
      });


      this.cards = [
        {
          title: "Total Clients",
          value: this.allProductBufferLevels.length.toString(),
          description: "Active clients in the system",
          icon: "pi pi-users"
        },
        {
          title: "Unverified Clients",
          value: this.allProductBufferLevels.filter(c => c.is_verified === false).length.toString(),
          description: "Unverified clients in the system",
          icon: "pi pi-clock"
        },
        {
          title: "Verified Clients",
          value: this.allProductBufferLevels.filter(c => c.is_verified === true).length.toString(),
          description: "Verified clients in the system",
          icon: "pi pi-verified"
        }
      ]
      this.loadingService.setLoadingState(false);
      this.loading = false;
    })
  }


  viewProductBufferLevel(productBufferLevel: UserDTO) {
    if (productBufferLevel) {
      this.selectedProductBufferLevel = productBufferLevel;
      this.showEditProductBufferLevelDialog = true;
    }
  }


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


  getStatusSeverityAndWord(status: Boolean) {
    switch (status) {
      case false:
        return { severity: 'danger' as const, status: 'Unverified' };

      case true:
        return { severity: 'success' as const, status: 'Verified' };

      default:
        return { severity: 'info' as const, status: 'Unknown' };
    }
  }


  updateCardNumbers(dt: Table) {
    const data = dt.filteredValue || this.allProductBufferLevels;
    this.cards = [
      {
        title: "Total Clients",
        value: this.allProductBufferLevels.length.toString(),
        description: "Active clients in the system",
        icon: "pi pi-users"
      },
      {
        title: "Unverified Clients",
        value: this.allProductBufferLevels.filter(c => c.is_verified === false).length.toString(),
        description: "Unverified clients in the system",
        icon: "pi pi-clock"
      },
      {
        title: "Verified Clients",
        value: this.allProductBufferLevels.filter(c => c.is_verified === true).length.toString(),
        description: "Verified clients in the system",
        icon: "pi pi-verified"
      }
    ]
  }

}
