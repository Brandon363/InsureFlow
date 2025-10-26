import { Injectable } from '@angular/core';
import { ClaimApprovalRequest, ClaimDTO, ClaimResponse } from '../models/claim.interface';
import { environment } from '../../environments/environment';
import { BehaviorSubject, map, Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ClaimService {
private baseURL = environment.baseUrl;
  private subUrl = 'claim';
  private allActiveClaims = new BehaviorSubject<ClaimDTO[]>([]);


  public selectedClaim!: ClaimDTO;

  constructor(
    private httpclient: HttpClient
  ) { }


  mapToResponse(data: any): ClaimResponse {
    return {
      success: data.success,
      statusCode: data.status_code,
      message: data.message,
      errors: data.errors || null,
      claim: data.claim || null,
      claims: data.claims || null,
      notifications: data.notifications || null,
      notification: data.notification || null,
    };
  }

  
  updateClaimData(configs: ClaimDTO[] | ClaimDTO) {
    if (Array.isArray(configs)) {
      this.allActiveClaims.next(configs);
    } else {
      const current = this.allActiveClaims.getValue();
      current.push(configs);
      this.allActiveClaims.next(current);
    }
  }


  retrieveClaimData(): Observable<ClaimDTO[]> {
    return this.allActiveClaims.asObservable();
  }

 
  getAllActiveClaims(): Observable<ClaimResponse> {
    return this.httpclient.get(`${this.baseURL}/${this.subUrl}/get-all-active-claims`).pipe(
      map((response: any) => {
        // console.log(response)
        const ClaimResponse = this.mapToResponse(response);
        if (ClaimResponse.success && ClaimResponse.claims) {
          this.updateClaimData(ClaimResponse.claims);
        }
        return ClaimResponse;
      })
    )
  }
 
  
  getAllActiveUserClaims(user_id: number): Observable<ClaimResponse> {
    return this.httpclient.get(`${this.baseURL}/${this.subUrl}/get-all-active-user-claims/` + user_id).pipe(
      map((response: any) => {
        // console.log(response)
        const ClaimResponse = this.mapToResponse(response);
        if (ClaimResponse.success && ClaimResponse.claims) {
          this.updateClaimData(ClaimResponse.claims);
        }
        return ClaimResponse;
      })
    )
  }


  editClaim(id: number, updateRequest: ClaimDTO): Observable<ClaimResponse> {
    return this.httpclient.put(`${this.baseURL}/${this.subUrl}/update-claim/${id}`, updateRequest).pipe(
      map((response: any) => {
        const ClaimResponse = this.mapToResponse(response);
        if (ClaimResponse.success && ClaimResponse.claim) {
          const current = this.allActiveClaims.getValue();
          const updated = current.map((p: any) =>
            p.id === ClaimResponse.claim?.id ? ClaimResponse.claim : p
          );
          this.allActiveClaims.next(updated);
        }

        return ClaimResponse;
      })
    );
  }


  approveClaim(request: ClaimApprovalRequest): Observable<ClaimResponse> {
    return this.httpclient.put(`${this.baseURL}/${this.subUrl}/verify-claim`, request).pipe(
      map((response: any) => {
        const ClaimResponse = this.mapToResponse(response);
        if (ClaimResponse.success && ClaimResponse.claim) {
          const current = this.allActiveClaims.getValue();
          const updated = current.map((p: any) =>
            p.id === ClaimResponse.claim?.id ? ClaimResponse.claim : p
          );
          this.allActiveClaims.next(updated);
        }

        return ClaimResponse;
      })
    );
  }


  rejectClaim(request: ClaimApprovalRequest): Observable<ClaimResponse> {
    return this.httpclient.put(`${this.baseURL}/${this.subUrl}/reject-claim`, request).pipe(
      map((response: any) => {
        const ClaimResponse = this.mapToResponse(response);
        if (ClaimResponse.success && ClaimResponse.claim) {
          const current = this.allActiveClaims.getValue();
          const updated = current.map((p: any) =>
            p.id === ClaimResponse.claim?.id ? ClaimResponse.claim : p
          );
          this.allActiveClaims.next(updated);
        }

        return ClaimResponse;
      })
    );
  }


  deleteClaimById(id: number): Observable<ClaimResponse> {
    return this.httpclient.delete(`${this.baseURL}/${this.subUrl}/delete-claim/${id}`).pipe(
      map((response: any) => {
        console.log(response)
        const ClaimResponse = this.mapToResponse(response);
        if (ClaimResponse.success && ClaimResponse.claim) {
          const current = this.allActiveClaims.getValue();
          const updated = current.filter(p => p.id !== ClaimResponse.claim?.id);
          this.allActiveClaims.next(updated);
        }

        return ClaimResponse;
      })
    );
  }


  getByClaimId(id: number): Observable<ClaimResponse> {
    return this.httpclient.get(`${this.baseURL}/${this.subUrl}/get-active-claim-by-id/${id}`).pipe(
      map((response: any) => {
        const ClaimResponse = this.mapToResponse(response);
        return ClaimResponse;
      })
    )
  }

  createClaim(createRequest: ClaimDTO): Observable<ClaimResponse> {
    return this.httpclient.post(`${this.baseURL}/${this.subUrl}/create-claim`, createRequest).pipe(
      map((response: any) => {
        console.log(response)
        const ClaimResponse = this.mapToResponse(response);
        if (ClaimResponse.success && ClaimResponse.claim) {
          this.updateClaimData(ClaimResponse.claim);
        }
        return ClaimResponse;
      })
    );
  }

}