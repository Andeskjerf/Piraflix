import axios from 'axios'
import { Room } from '@/api/models/RoomModel'
import config from '../../config/hosts.json'

const apiRoomPath = config.httpType + '://' + config.ip + ':' + config.backendPort + '/api/rooms'

export async function createRoom (magnet: string): Promise<Room> {
  try {
    const response = await axios.post(apiRoomPath, { magnet: magnet }, { withCredentials: true })
    const parsed = JSON.parse(response.data.room)
    return new Room(parsed.id, parsed.paused, parsed.timestamp, parsed.magnet)
  } catch (error) {
    console.log(error)
    return new Room()
  }
}

export async function getRoom (roomId: string): Promise<Room> {
  try {
    const response = await axios.get(apiRoomPath + '?roomId=' + roomId, { withCredentials: true })
    const parsed = JSON.parse(response.data.room)
    return new Room(parsed.id, parsed.paused, parsed.timestamp, parsed.magnet)
  } catch (error) {
    return new Room()
  }
}
