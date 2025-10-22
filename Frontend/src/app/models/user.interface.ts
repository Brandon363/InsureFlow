import { EntityStatus } from "./enum.interface";
import { ExtractedUserDTO } from "./extracted_user.interface";
import { BaseResponse, UserRole } from "./shared.interface";

export interface UserDTO {
  id: number;
  id_number: string;
  email: string;
  first_name: string;
  last_name: string;
  other_names?: string;
  user_role: UserRole;
  date_of_birth: Date;
  village_of_origin: string;
  place_of_birth: string;
  phone_number?: string;
  address?: string;
  is_logged_in: boolean;
  is_verified?: boolean;
  extracted_user?: ExtractedUserDTO;
  date_last_logged_in?: Date;
  date_created: Date;
  date_updated?: Date;
  entity_status: EntityStatus;

}

export interface TokenData {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  user_role: UserRole;
//   is_logged_in: boolean;
  date_created: Date;
  date_updated?: Date;
  entity_status: EntityStatus;
}

export interface UserCreateRequest {
  id_number: string;
  email: string;
  first_name: string;
  last_name: string;
  other_names?: string;
  user_role: UserRole;
  date_of_birth: Date;
  village_of_origin: string;
  place_of_birth: string;
  phone_number?: string;
  address?: string;
  password: string;
}

export interface UserUpdateRequest {
  id: number;
  id_number?: string;
  email?: string;
  first_name?: string;
  last_name?: string;
  user_role?: UserRole;
  other_names?: UserRole;
  phone_number?: string;
  address?: string;
  date_of_birth?: Date;
  village_of_origin?: string;
  place_of_birth?: string;
  is_logged_in?: boolean;
}

export interface UserLoginRequest {
  email: string;
  password: string;
}

export interface UserPasswordUpdate {
  oldPassword: string;
  newPassword: string;
}

export interface UserResponse extends BaseResponse {
  user?: UserDTO;
  users?: UserDTO[];
}