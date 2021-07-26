import axios from 'axios'
import { Room } from '@/api/models/RoomModel'

const apiRoomPath = 'http://127.0.0.1:5000/api/rooms'

export async function createRoom (magnet: string): Promise<Room> {
  try {
    const response = await axios.post(apiRoomPath, { magnet: magnet })
    const parsed = JSON.parse(response.data.room)
    return new Room(parsed.id, parsed.paused, parsed.timestamp, parsed.magnet)
  } catch (error) {
    console.log(error)
    return new Room()
  }
}

export async function getRoom (roomId: string): Promise<Room> {
  try {
    const response = await axios.get(apiRoomPath + '?roomId=' + roomId)
    const parsed = JSON.parse(response.data.room)
    return new Room(parsed.id, parsed.paused, parsed.timestamp, parsed.magnet)
  } catch (error) {
    console.log(error)
    return new Room()
  }
}
