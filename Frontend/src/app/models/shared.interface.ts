export interface BaseResponse {
  statusCode: number;
  success: boolean;
  message: string;
  errors?: ErrorDetail[] | null;
}

export interface ErrorDetail {
  field: string;
  message: string;
}


export interface UserRole {
 
}



export interface MenuDto {
  path: string;
  icon: string;
  text: string;
  buttonClass: string;
  tooltip: string;
  rippleColor: string;
  roles: Array<string>
}