import { atom } from 'jotai'

export const updateDataState = atom(false)

export const timeState = atom(new Date("2024-09-25T01:00:00.000Z"))

export const elevationState = atom(10)

export const gnssState = atom({
    GPS: true,
    GLONASS: true,
    Galileo: true,
    BeiDou: true,
    QZSS: true,
    NavIC: true,
    SBAS:true,
  })