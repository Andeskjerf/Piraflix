import axios from 'axios'
import config from '../../config/hosts.json'

const apiRoomPath = config.httpType + '://' + config.ip + ':' + config.backendPort + '/cookie'

export async function checkCookie (): Promise<void> {
  try {
    await axios.get(apiRoomPath, { withCredentials: true })
    // const parsed = JSON.parse(response.data.room)
    // return new Room(parsed.id, parsed.paused, parsed.timestamp, parsed.magnet)
  } catch (error) {
    console.log(error)
    // return new Room()
  }
}
