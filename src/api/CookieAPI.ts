import axios from 'axios'
import config from '../../config/hosts.json'

const apiRoomPath = config.httpType + '://' + config.ip + ':' + config.backendPort + '/cookie'

export async function checkCookie (): Promise<void> {
  try {
    await axios.get(apiRoomPath, { withCredentials: true })
  } catch (error) {
    console.log(error)
  }
}
