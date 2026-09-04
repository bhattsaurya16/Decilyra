export class ApiError extends Error {
  constructor(
    public readonly status: number,
    message: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

async function errorMessage(response: Response, path: string): Promise<string> {
  try {
    const payload = (await response.json()) as { error?: { message?: string } };
    return payload.error?.message ?? `Request failed: ${response.status} ${path}`;
  } catch {
    return `Request failed: ${response.status} ${path}`;
  }
}

function getBaseUrl(): string {
  const url = process.env.NEXT_PUBLIC_API_URL;
  if (!url) {
    throw new Error("NEXT_PUBLIC_API_URL is not configured.");
  }
  return url.replace(/\/$/, "");
}

export async function apiGet<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${getBaseUrl()}${path}`, {
    ...init,
    method: "GET",
    headers: {
      Accept: "application/json",
      ...init?.headers,
    },
    cache: "no-store",
  });

  if (!response.ok) {
    throw new ApiError(response.status, await errorMessage(response, path));
  }

  return (await response.json()) as T;
}

export async function apiSend<T>(path: string, init: RequestInit): Promise<T> {
  const isForm = init.body instanceof FormData;
  const response = await fetch(`${getBaseUrl()}${path}`, {
    ...init,
    headers: {
      Accept: "application/json",
      ...(!isForm ? { "Content-Type": "application/json" } : {}),
      ...init.headers,
    },
  });

  if (!response.ok) {
    throw new ApiError(response.status, await errorMessage(response, path));
  }

  return (await response.json()) as T;
}
