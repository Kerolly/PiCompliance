export interface Port {
  port: number;
  state: string;
  service: string;
  product: string | null;
  version: string | null;
  extrainfo: string | null;
}

export interface Device {
  ip: string;
  mac: string;
  vendor: string;
  hostname: string;
  os: string | null;
  ports: Port[];
}
