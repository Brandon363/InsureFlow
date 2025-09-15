// import { HttpEvent, HttpHandler, HttpInterceptor, HttpInterceptorFn, HttpRequest } from '@angular/common/http';
// import { Injectable } from '@angular/core';
// import { AuthService } from '../services/auth.service';
// import { Observable } from 'rxjs';

// export const authInterceptor: HttpInterceptorFn = (req, next) => {
//   return next(req);
// };

//  @Injectable()
// export class AuthInterceptor implements HttpInterceptor {
//   constructor(private authService: AuthService) {}

//   intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
//     const token = this.authService.getToken();
//     if (token) {
//       const cloned = req.clone({
//         headers: req.headers.set('Authorization', 'Bearer ' + token)
//       });
//       return next.handle(cloned);
//     } else {
//       return next.handle(req);
//     }
//   }
// }

import { inject } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { HttpInterceptorFn } from '@angular/common/http';

// export const authInterceptor: HttpInterceptorFn = (req, next) => {
//   const authService = inject(AuthService);
//   const token = authService.getToken();
//   // console.log(req)
//   if (token) {
//     const clonedReq = req.clone({
//       headers: req.headers.set('Authorization', `Bearer ${token}`)
//     });

//     return next(clonedReq);
//   }

  
//   return next(req);
// };
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const reqWithCreds = req.clone({ withCredentials: true });
  return next(reqWithCreds);
};
