export default class RateLimiter {
  constructor(maxRequestsPerMinute, userLimit = null) {
    this.maxRequestsPerMinute = maxRequestsPerMinute
    this.userLimit = userLimit || maxRequestsPerMinute
    this.requestTimestamps = []
  }

  async waitForSlot() {
    const now = Date.now()
    const oneMinuteAgo = now - 60000

    // Remove timestamps older than 1 minute
    this.requestTimestamps = this.requestTimestamps.filter(timestamp => timestamp > oneMinuteAgo)

    if (this.requestTimestamps.length >= this.userLimit) {
      const oldestTimestamp = this.requestTimestamps[0]
      const timeToWait = 60000 - (now - oldestTimestamp)
      await new Promise(resolve => setTimeout(resolve, timeToWait))
    }
    this.requestTimestamps.push(Date.now())
  }
}
