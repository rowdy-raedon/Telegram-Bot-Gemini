import os
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich import print as rprint
from dotenv import load_dotenv

from mailsac import MailsacAPI
from gemini import GeminiClient
from utils import generate_random_email, format_timestamp, truncate_text, extract_plain_text

# Load environment variables
load_dotenv()

class TempEmailApp:
    """Main application class for the temporary email service."""
    
    def __init__(self):
        """Initialize the application."""
        self.console = Console()
        self.current_email = None
        self.mailsac_client = None
        self.gemini_client = None
        self._setup_clients()
    
    def _setup_clients(self):
        """Set up API clients."""
        mailsac_key = os.getenv('MAILSAC_API_KEY')
        gemini_key = os.getenv('GEMINI_API_KEY')
        
        if not mailsac_key or mailsac_key == 'your_mailsac_api_key_here':
            self.console.print("[red]Error: Please set your MAILSAC_API_KEY in the .env file[/red]")
            return False
            
        if not gemini_key or gemini_key == 'your_gemini_api_key_here':
            self.console.print("[red]Error: Please set your GEMINI_API_KEY in the .env file[/red]")
            return False
        
        try:
            self.mailsac_client = MailsacAPI(mailsac_key)
            self.gemini_client = GeminiClient(gemini_key)
            return True
        except Exception as e:
            self.console.print(f"[red]Error initializing clients: {str(e)}[/red]")
            return False
    
    def _display_welcome(self):
        """Display welcome message and instructions."""
        welcome_text = """
[bold blue]🔑 Temporary Email Service[/bold blue]

This application provides a temporary email service using Mailsac API with AI-powered features via Gemini.

[bold]Available Commands:[/bold]
• [cyan]inbox[/cyan] - View all emails in your inbox
• [cyan]read <message_id>[/cyan] - Read a specific email
• [cyan]summarize <message_id>[/cyan] - Get AI summary of an email
• [cyan]ask <message_id> "<question>"[/cyan] - Ask AI about email content
• [cyan]delete <message_id>[/cyan] - Delete an email
• [cyan]new_address[/cyan] - Switch to a different email address
• [cyan]help[/cyan] - Show this help message
• [cyan]exit[/cyan] - Exit the application
        """
        
        panel = Panel(welcome_text, border_style="blue", padding=(1, 2))
        self.console.print(panel)
    
    def _setup_email_address(self):
        """Set up the email address to use."""
        self.console.print("\n[bold]Email Address Setup[/bold]")
        
        choice = Prompt.ask(
            "Would you like to",
            choices=["generate", "enter"],
            default="generate"
        )
        
        if choice == "generate":
            self.current_email = generate_random_email()
            self.console.print(f"[green]Generated email address: {self.current_email}[/green]")
        else:
            email = Prompt.ask("Enter your Mailsac email address")
            if "@" not in email:
                email += "@mailsac.com"
            self.current_email = email
            self.console.print(f"[green]Using email address: {self.current_email}[/green]")
    
    def _display_inbox(self):
        """Display the inbox with all messages."""
        if not self.current_email:
            self.console.print("[red]No email address selected[/red]")
            return
        
        try:
            with self.console.status(f"[bold green]Fetching emails for {self.current_email}..."):
                messages = self.mailsac_client.get_messages(self.current_email)
            
            if not messages:
                self.console.print("[yellow]No messages found in inbox[/yellow]")
                return
            
            table = Table(title=f"Inbox for {self.current_email}")
            table.add_column("ID", style="cyan", width=12)
            table.add_column("From", style="green", width=30)
            table.add_column("Subject", style="white", width=40)
            table.add_column("Date", style="blue", width=20)
            
            for msg in messages:
                message_id = msg.get('_id', 'N/A')[:10]
                sender = truncate_text(msg.get('from', [{}])[0].get('address', 'Unknown'), 28)
                subject = truncate_text(msg.get('subject', 'No Subject'), 38)
                date = format_timestamp(msg.get('received', 'Unknown'))
                
                table.add_row(message_id, sender, subject, date)
            
            self.console.print(table)
            
        except Exception as e:
            self.console.print(f"[red]Error fetching inbox: {str(e)}[/red]")
    
    def _read_message(self, message_id: str):
        """Read a specific message."""
        if not self.current_email:
            self.console.print("[red]No email address selected[/red]")
            return
        
        try:
            with self.console.status(f"[bold green]Reading message {message_id}..."):
                message = self.mailsac_client.get_message_body(self.current_email, message_id)
            
            # Display message details
            sender = message.get('from', [{}])[0].get('address', 'Unknown')
            subject = message.get('subject', 'No Subject')
            date = format_timestamp(message.get('received', 'Unknown'))
            
            self.console.print(f"\n[bold]From:[/bold] {sender}")
            self.console.print(f"[bold]Subject:[/bold] {subject}")
            self.console.print(f"[bold]Date:[/bold] {date}")
            self.console.print("-" * 60)
            
            # Display message body
            body = extract_plain_text(message.get('body', 'No content'))
            panel = Panel(body, border_style="green", title="Message Content")
            self.console.print(panel)
            
        except Exception as e:
            self.console.print(f"[red]Error reading message: {str(e)}[/red]")
    
    def _summarize_message(self, message_id: str):
        """Summarize a message using AI."""
        if not self.current_email:
            self.console.print("[red]No email address selected[/red]")
            return
        
        try:
            with self.console.status(f"[bold green]Getting message content..."):
                message = self.mailsac_client.get_message_body(self.current_email, message_id)
            
            body = extract_plain_text(message.get('body', 'No content'))
            subject = message.get('subject', 'No Subject')
            
            email_content = f"Subject: {subject}\n\nContent: {body}"
            
            with self.console.status(f"[bold blue]AI is summarizing the message..."):
                summary = self.gemini_client.summarize_email(email_content)
            
            panel = Panel(summary, border_style="blue", title="📝 AI Summary")
            self.console.print(panel)
            
        except Exception as e:
            self.console.print(f"[red]Error summarizing message: {str(e)}[/red]")
    
    def _ask_about_message(self, message_id: str, question: str):
        """Ask AI a question about a message."""
        if not self.current_email:
            self.console.print("[red]No email address selected[/red]")
            return
        
        try:
            with self.console.status(f"[bold green]Getting message content..."):
                message = self.mailsac_client.get_message_body(self.current_email, message_id)
            
            body = extract_plain_text(message.get('body', 'No content'))
            subject = message.get('subject', 'No Subject')
            
            email_content = f"Subject: {subject}\n\nContent: {body}"
            
            with self.console.status(f"[bold blue]AI is analyzing the message..."):
                answer = self.gemini_client.answer_question_about_email(email_content, question)
            
            self.console.print(f"\n[bold]Question:[/bold] {question}")
            panel = Panel(answer, border_style="blue", title="🤖 AI Answer")
            self.console.print(panel)
            
        except Exception as e:
            self.console.print(f"[red]Error asking about message: {str(e)}[/red]")
    
    def _delete_message(self, message_id: str):
        """Delete a message."""
        if not self.current_email:
            self.console.print("[red]No email address selected[/red]")
            return
        
        if not Confirm.ask(f"Are you sure you want to delete message {message_id}?"):
            return
        
        try:
            with self.console.status(f"[bold red]Deleting message {message_id}..."):
                self.mailsac_client.delete_message(self.current_email, message_id)
            
            self.console.print(f"[green]Message {message_id} deleted successfully[/green]")
            
        except Exception as e:
            self.console.print(f"[red]Error deleting message: {str(e)}[/red]")
    
    def _parse_command(self, command: str):
        """Parse and execute a command."""
        parts = command.strip().split(' ', 2)
        cmd = parts[0].lower()
        
        if cmd == 'inbox':
            self._display_inbox()
        
        elif cmd == 'read':
            if len(parts) < 2:
                self.console.print("[red]Usage: read <message_id>[/red]")
                return
            self._read_message(parts[1])
        
        elif cmd == 'summarize':
            if len(parts) < 2:
                self.console.print("[red]Usage: summarize <message_id>[/red]")
                return
            self._summarize_message(parts[1])
        
        elif cmd == 'ask':
            if len(parts) < 3:
                self.console.print("[red]Usage: ask <message_id> \"<question>\"[/red]")
                return
            question = parts[2].strip('"\'')
            self._ask_about_message(parts[1], question)
        
        elif cmd == 'delete':
            if len(parts) < 2:
                self.console.print("[red]Usage: delete <message_id>[/red]")
                return
            self._delete_message(parts[1])
        
        elif cmd == 'new_address':
            self._setup_email_address()
        
        elif cmd == 'help':
            self._display_welcome()
        
        elif cmd == 'exit':
            return False
        
        else:
            self.console.print(f"[red]Unknown command: {cmd}. Type 'help' for available commands.[/red]")
        
        return True
    
    def run(self):
        """Run the main application loop."""
        if not self.mailsac_client or not self.gemini_client:
            return
        
        self._display_welcome()
        self._setup_email_address()
        
        self.console.print(f"\n[green]Ready! Current email: {self.current_email}[/green]")
        self.console.print("[dim]Type 'help' for commands or 'exit' to quit[/dim]\n")
        
        while True:
            try:
                command = Prompt.ask("[bold cyan]>[/bold cyan]", default="inbox")
                
                if not self._parse_command(command):
                    break
                    
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Goodbye![/yellow]")
                break
            except Exception as e:
                self.console.print(f"[red]Unexpected error: {str(e)}[/red]")


if __name__ == "__main__":
    app = TempEmailApp()
    app.run()