export class Room {
  id: string;
  paused: boolean;
  timestamp: number;
  magnet: string;

  constructor (id = '-1', paused = false, timestamp = -1, magnet = '') {
    this.id = id
    this.paused = paused
    this.timestamp = timestamp
    this.magnet = magnet
  }
}
