export class UserModel {
  identifier: string
  username: string

  constructor (identifier = '-1', username = 'null') {
    this.identifier = identifier
    this.username = username
  }
}
