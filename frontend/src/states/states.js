import { atom } from 'jotai'

export const updateDataState = atom(false)

export const timeState = atom(new Date())

export const epochState = atom(2)
export const elevationState = atom(10)

export const gnssState = atom({
    GPS: true,
    GLONASS: true,
    Galileo: true,
    BeiDou: true,
    QZSS: true,
    NavIC: true,
    SBAS:false,
  })

export const gnssState2 = atom({
    GPS: true,
    GLONASS: true,
    Galileo: true,
    BeiDou: true,
    QZSS: true,
    NavIC: true,
    SBAS:false,
  })